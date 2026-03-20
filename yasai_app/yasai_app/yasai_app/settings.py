from pathlib import Path
import os

# プロジェクトのベースディレクトリを設定
BASE_DIR = Path(__file__).resolve().parent.parent

# シークレットキー（本番環境では環境変数から読み込むべき）
SECRET_KEY = 'django-insecure-9=4xyx*w1+7&8pb#&w*4_@2jgv3va8li+nr_a_g(4=3zjeo__k'

# デバッグモード（本番環境では環境変数でFalseにする）
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

# アクセスを許可するホスト名（*は全て許可）
ALLOWED_HOSTS = ['*']

# このプロジェクトで使うアプリの一覧
INSTALLED_APPS = [
    'django.contrib.admin',    # 管理画面
    'django.contrib.auth',     # 認証・ログイン機能
    'django.contrib.contenttypes',
    'django.contrib.sessions', # セッション管理
    'django.contrib.messages', # メッセージ機能
    'django.contrib.staticfiles', # 静的ファイル管理
    'plants',                  # 自分で作ったアプリ
]

# リクエストとレスポンスの間に挟まる処理の一覧
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',          # セキュリティ対策
    'whitenoise.middleware.WhiteNoiseMiddleware',             # 静的ファイルを配信する
    'django.contrib.sessions.middleware.SessionMiddleware',  # セッション管理
    'django.middleware.common.CommonMiddleware',             # 共通処理
    'django.middleware.csrf.CsrfViewMiddleware',             # CSRF対策（フォームのセキュリティ）
    'django.contrib.auth.middleware.AuthenticationMiddleware', # 認証処理
    'django.contrib.messages.middleware.MessageMiddleware',  # メッセージ処理
    'django.middleware.clickjacking.XFrameOptionsMiddleware', # クリックジャッキング対策
]

# URLの設定ファイルの場所
ROOT_URLCONF = 'yasai_app.urls'

# テンプレート（HTML）の設定
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True, # アプリのtemplatesフォルダを自動で探す
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# 本番環境用サーバーの設定ファイルの場所
WSGI_APPLICATION = 'yasai_app.wsgi.application'

# データベースの設定（開発中はSQLiteを使用）
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # SQLiteを使う
        'NAME': BASE_DIR / 'db.sqlite3',        # データベースファイルの場所
    }
}

# パスワードのバリデーション（強度チェック）設定
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    }, # ユーザー名と似たパスワードを禁止
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    }, # 最低文字数のチェック
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    }, # よくあるパスワードを禁止
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    }, # 数字だけのパスワードを禁止
]

# 言語設定
LANGUAGE_CODE = 'ja' # 日本語に変更

# タイムゾーン設定
TIME_ZONE = 'Asia/Tokyo' # 日本時間に変更

USE_I18N = True # 国際化機能を有効にする

USE_TZ = True # タイムゾーンを有効にする

# 静的ファイル（CSS・画像など）のURL
STATIC_URL = 'static/'

# 静的ファイルを集める場所（本番環境用）
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# whitenoise で静的ファイルを圧縮して配信する設定
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

import dj_database_url
# 本番環境ではDATABASE_URLという環境変数からDBの設定を読み込む
if os.environ.get('DATABASE_URL'):
    DATABASES['default'] = dj_database_url.config(conn_max_age=600)