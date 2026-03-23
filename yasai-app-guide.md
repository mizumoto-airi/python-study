# Django 野菜育成計画アプリ 開発ガイド

## 目次
1. [Djangoとは？](#djangoとは)
2. [使用技術](#使用技術)
3. [環境構築](#環境構築)
4. [フォルダ構成](#フォルダ構成)
5. [MVTとは？](#mvtとは)
6. [実装手順](#実装手順)
   - [Step1: プロジェクト作成](#step1-プロジェクト作成)
   - [Step2: アプリ作成](#step2-アプリ作成)
   - [Step3: モデルの作成](#step3-モデルの作成)
   - [Step4: 管理画面の設定](#step4-管理画面の設定)
   - [Step5: ビューの作成](#step5-ビューの作成)
   - [Step6: URLの設定](#step6-urlの設定)
   - [Step7: フォームの作成](#step7-フォームの作成)
   - [Step8: テンプレートの作成](#step8-テンプレートの作成)
   - [Step9: Renderにデプロイ](#step9-renderにデプロイ)
7. [つまずきポイント集](#つまずきポイント集)

---

## Djangoとは？

DjangoはPythonのWebフレームワークです。
「バッテリー同梱（batteries included）」と呼ばれるほど最初から機能が豊富です。

**特徴**
- 管理画面が自動生成される
- ログイン・認証機能が最初から入っている
- データベース操作が簡単にできる
- セキュリティ対策が最初から入っている

**RailsとDjangoの比較**

| 機能 | Ruby on Rails | Django |
|------|--------------|--------|
| ルーティング | `routes.rb` | `urls.py` |
| データ設計 | `migration` | `models.py` |
| 画面の処理 | `Controller` | `views.py` |
| HTML | `View（erb）` | `Template（html）` |
| 管理画面 | 別途作成 | **自動生成！** |
| ログイン機能 | 別途作成 | **最初から入っている！** |

---

## 使用技術

| 技術 | 用途 |
|------|------|
| Python 3.12 | プログラミング言語 |
| Django 6.0 | Webフレームワーク |
| Bootstrap 5 | CSSライブラリ（デザイン） |
| SQLite | 開発用データベース |
| gunicorn | 本番環境用サーバー |
| whitenoise | 静的ファイル配信 |
| Render | ホスティングサービス（デプロイ先） |

---

## 環境構築

### 1. Pythonのバージョン確認

```powershell
python --version
```

### 2. Djangoのインストール

```powershell
pip install django
django-admin --version  # バージョン確認
```

### 3. 本番環境用ライブラリのインストール

```powershell
pip install gunicorn whitenoise dj-database-url psycopg2-binary python-dotenv
```

| ライブラリ | 役割 |
|-----------|------|
| `gunicorn` | 本番環境用のサーバー |
| `whitenoise` | 静的ファイル（CSS・画像）を配信する |
| `dj-database-url` | データベースのURLを読み込む |
| `psycopg2-binary` | PostgreSQL（本番用DB）に接続する |
| `python-dotenv` | 環境変数を管理する |

---

## フォルダ構成

```
yasai_app/                    ← プロジェクト全体のフォルダ
├── plants/                   ← 野菜管理アプリ
│   ├── migrations/           ← データベースの変更履歴
│   ├── templates/
│   │   └── plants/
│   │       ├── plant_list.html          # 一覧ページ
│   │       ├── plant_form.html          # 追加フォーム
│   │       ├── plant_detail.html        # 詳細ページ
│   │       └── plant_confirm_delete.html # 削除確認ページ
│   ├── admin.py              ← 管理画面の設定
│   ├── apps.py               ← アプリの設定
│   ├── forms.py              ← フォームの設定
│   ├── models.py             ← データベースのテーブル設計
│   ├── urls.py               ← URLのルーティング
│   └── views.py              ← 画面に表示する処理
├── yasai_app/                ← プロジェクトの設定フォルダ
│   ├── settings.py           ← アプリ全体の設定
│   ├── urls.py               ← プロジェクト全体のURLルーティング
│   └── wsgi.py               ← 本番環境用ファイル
├── manage.py                 ← Djangoの操作コマンドを実行するファイル
├── Procfile                  ← Renderの起動コマンド設定
└── requirements.txt          ← 使用ライブラリの一覧
```

---

## MVTとは？

DjangoはMVT（Model・View・Template）という構造で動いています。

| 名前 | ファイル | 役割 |
|------|---------|------|
| Model（モデル） | `models.py` | データベースのテーブル設計 |
| View（ビュー） | `views.py` | 処理のロジック |
| Template（テンプレート） | `*.html` | 画面のHTML |

**リクエストの流れ**
```
ブラウザ
  ↓ URLにアクセス
urls.py（どのviewを呼ぶか判断）
  ↓
views.py（データを取得・処理）
  ↓ models.pyでDBからデータ取得
templates/（HTMLに変換して返す）
  ↓
ブラウザ（画面が表示される）
```

---

## 実装手順

### Step1: プロジェクト作成

```powershell
django-admin startproject yasai_app
cd yasai_app
python manage.py runserver  # 開発サーバー起動
```

ブラウザで `http://127.0.0.1:8000/` を開いてロケットの画面が出ればOKです！

> ⚠️ **注意**
> PCを再起動したり、PowerShellを閉じた後は毎回 `python manage.py runserver` が必要です。

---

### Step2: アプリ作成

```powershell
python manage.py startapp plants
```

作成したら `yasai_app/settings.py` の `INSTALLED_APPS` に追加します。

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'plants',  # 追加！
]
```

> 💡 **DjangoのプロジェクトとアプリはRailsと違う概念です**
> - **プロジェクト** → 全体の箱（`yasai_app`）
> - **アプリ** → 機能ごとの部品（`plants`）

---

### Step3: モデルの作成

`plants/models.py` を作成します。

```python
from django.db import models

class Plant(models.Model):
    name = models.CharField(max_length=100)        # 野菜の名前
    season = models.CharField(max_length=50)       # 育てる季節
    sow_month = models.IntegerField()              # 種まきの月
    harvest_month = models.IntegerField()          # 収穫の月
    days_to_harvest = models.IntegerField()        # 収穫までの日数
    memo = models.TextField(blank=True)            # メモ（空でもOK）
    created_at = models.DateTimeField(auto_now_add=True)  # 登録日時

    def __str__(self):
        return self.name  # 管理画面などで表示する名前
```

**よく使うフィールドの種類**

| フィールド | 意味 |
|-----------|------|
| `CharField` | 短い文字列（名前など） |
| `TextField` | 長い文字列（メモなど） |
| `IntegerField` | 整数 |
| `DateTimeField` | 日時 |
| `BooleanField` | 真偽値 |
| `ForeignKey` | 他のモデルとの関連（外部キー） |

**オプション**

| オプション | 意味 |
|-----------|------|
| `blank=True` | 空でもOK |
| `null=True` | NULLを許可 |
| `auto_now_add=True` | 作成時の日時を自動で保存 |
| `max_length=100` | 最大文字数 |

モデルを作ったらデータベースに反映します。

```powershell
python manage.py makemigrations  # 変更をファイルに変換
python manage.py migrate         # データベースに反映
```

> 💡 **makemigrationsとmigrateの違い**
> - `makemigrations` → レシピを作る
> - `migrate` → レシピを見ながら実際に料理する

---

### Step4: 管理画面の設定

`plants/admin.py` を編集します。

```python
from django.contrib import admin
from .models import Plant

admin.site.register(Plant)  # 管理画面にPlantを登録
```

スーパーユーザーを作成します。

```powershell
python manage.py createsuperuser
```

ブラウザで `http://127.0.0.1:8000/admin/` を開いてログインすると管理画面が使えます！

> 💡 **Djangoの管理画面が自動でやってくれること**
> - フォームの自動生成
> - 一覧・追加・編集・削除
> - バリデーション（入力チェック）
> - ログイン認証

---

### Step5: ビューの作成

`plants/views.py` を作成します。

```python
from django.shortcuts import render, redirect, get_object_or_404
from .models import Plant
from .forms import PlantForm

# 一覧ページ
def plant_list(request):
    plants = Plant.objects.all()  # データベースから全件取得
    return render(request, 'plants/plant_list.html', {'plants': plants})

# 追加フォーム
def plant_create(request):
    if request.method == 'POST':        # フォームが送信されたとき
        form = PlantForm(request.POST)  # 送信データをフォームに入れる
        if form.is_valid():             # バリデーションチェック
            form.save()                 # データベースに保存
            return redirect('plant_list')  # 一覧ページに移動
    else:
        form = PlantForm()  # 空のフォームを表示
    return render(request, 'plants/plant_form.html', {'form': form})

# 詳細ページ
def plant_detail(request, pk):
    plant = get_object_or_404(Plant, pk=pk)  # IDでデータ取得（なければ404）
    return render(request, 'plants/plant_detail.html', {'plant': plant})

# 削除
def plant_delete(request, pk):
    plant = get_object_or_404(Plant, pk=pk)
    if request.method == 'POST':  # 削除確認後
        plant.delete()            # データベースから削除
        return redirect('plant_list')
    return render(request, 'plants/plant_confirm_delete.html', {'plant': plant})
```

**よく使うデータ取得方法**

| コード | 意味 |
|--------|------|
| `Plant.objects.all()` | 全件取得 |
| `Plant.objects.get(pk=1)` | IDで1件取得 |
| `Plant.objects.filter(season='夏')` | 条件で絞り込み |
| `get_object_or_404(Plant, pk=pk)` | IDで取得（なければ404） |

---

### Step6: URLの設定

**`yasai_app/urls.py`** を編集します。

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),        # 管理画面
    path('', include('plants.urls')),       # plantsアプリのURLに任せる
]
```

**`plants/urls.py`** を新規作成します。

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.plant_list, name='plant_list'),                    # 一覧
    path('create/', views.plant_create, name='plant_create'),         # 追加
    path('detail/<int:pk>/', views.plant_detail, name='plant_detail'), # 詳細
    path('delete/<int:pk>/', views.plant_delete, name='plant_delete'), # 削除
]
```

> 💡 **`<int:pk>` って何？**
> URLの中に数字を埋め込む書き方です。
> `http://127.0.0.1:8000/detail/1/` → ID:1のデータの詳細ページ

**RailsとDjangoのルーティング比較**

| Rails（routes.rb） | Django（urls.py） |
|-------------------|------------------|
| `resources :plants` | 1個ずつ手動で書く |
| `get '/plants', to: 'plants#index'` | `path('', views.plant_list)` |

---

### Step7: フォームの作成

`plants/forms.py` を新規作成します。

```python
from django import forms
from .models import Plant

class PlantForm(forms.ModelForm):
    class Meta:
        model = Plant  # Plantモデルを使う
        fields = ['name', 'season', 'sow_month', 'harvest_month', 'days_to_harvest', 'memo']
        labels = {
            'name': '野菜名',
            'season': '季節',
            'sow_month': '種まきの月',
            'harvest_month': '収穫の月',
            'days_to_harvest': '収穫までの日数',
            'memo': 'メモ',
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'border-radius: 10px; border: 2px solid #4caf50;',
                'placeholder': '例：トマト',
            }),
            'season': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'border-radius: 10px; border: 2px solid #4caf50;',
                'placeholder': '例：夏',
            }),
            'sow_month': forms.NumberInput(attrs={
                'class': 'form-control',
                'style': 'border-radius: 10px; border: 2px solid #4caf50;',
                'placeholder': '例：4',
            }),
            'harvest_month': forms.NumberInput(attrs={
                'class': 'form-control',
                'style': 'border-radius: 10px; border: 2px solid #4caf50;',
                'placeholder': '例：7',
            }),
            'days_to_harvest': forms.NumberInput(attrs={
                'class': 'form-control',
                'style': 'border-radius: 10px; border: 2px solid #4caf50;',
                'placeholder': '例：90',
            }),
            'memo': forms.Textarea(attrs={
                'class': 'form-control',
                'style': 'border-radius: 10px; border: 2px solid #4caf50;',
                'rows': 3,
                'placeholder': '自由にメモを書いてください',
            }),
        }
```

> 💡 **`ModelForm` の `Meta` クラスに書けるもの**
>
> | キーワード | 意味 |
> |-----------|------|
> | `model` | どのモデルを使うか |
> | `fields` | 表示する項目を指定 |
> | `exclude` | 除外する項目を指定 |
> | `labels` | 項目名を変える |
> | `widgets` | 入力欄のデザインを変える |
> | `help_texts` | 入力欄の下にヒント文を表示する |

---

### Step8: テンプレートの作成

Djangoのテンプレートは `{% %}` と `{{ }}` を使います。

| 記法 | 意味 |
|------|------|
| `{{ 変数名 }}` | 変数を表示する |
| `{% for x in list %}` | forループ |
| `{% endfor %}` | forループの終わり |
| `{% if 条件 %}` | 条件分岐 |
| `{% endif %}` | ifの終わり |
| `{% url '名前' %}` | URL名からURLを生成 |
| `{% csrf_token %}` | セキュリティ対策（フォームに必須） |

**一覧ページ（plant_list.html）の例**

```html
{% for plant in plants %}
<div>
  <h2>{{ plant.name }}</h2>
  <p>{{ plant.season }}</p>
  <a href="{% url 'plant_detail' plant.pk %}">詳細</a>
  <a href="{% url 'plant_delete' plant.pk %}">削除</a>
</div>
{% endfor %}
```

**追加フォーム（plant_form.html）の例**

```html
<form method="post">
  {% csrf_token %}
  {% for field in form %}
  <div>
    <label>{{ field.label }}</label>
    {{ field }}
  </div>
  {% endfor %}
  <button type="submit">保存する</button>
</form>
```

---

### Step9: Renderにデプロイ

#### 1. settings.py の本番環境用設定

```python
import os

# 本番環境ではFalseにする
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

# 全てのホストを許可
ALLOWED_HOSTS = ['*']

# whitenoise を MIDDLEWARE に追加
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # 追加！
    ...
]

# 静的ファイルを集める場所
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# whitenoise で静的ファイルを圧縮して配信
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# 本番環境ではPostgreSQLを使う
import dj_database_url
if os.environ.get('DATABASE_URL'):
    DATABASES['default'] = dj_database_url.config(conn_max_age=600)
```

#### 2. Procfile の作成

PowerShellで作成します（VSCodeでは作れないことがある）。

```powershell
New-Item Procfile -ItemType File
Set-Content Procfile "web: gunicorn yasai_app.wsgi"
```

#### 3. requirements.txt の作成

```powershell
pip freeze > requirements.txt
```

#### 4. GitHubにプッシュ

```powershell
git add .
git commit -m "Renderデプロイ準備"
git push origin main
```

#### 5. Renderの設定

| 項目 | 設定値 |
|------|--------|
| Repository | GitHubのリポジトリ |
| Branch | `main` |
| Root Directory | `yasai_app`（サブフォルダの場合） |
| Runtime | `Python 3` |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `gunicorn yasai_app.wsgi` |

---

## つまずきポイント集

### ❶ `python manage.py runserver` を忘れる

**症状**
ブラウザで「接続が拒否されました」と表示される。

**解決方法**
```powershell
cd yasai_app
python manage.py runserver
```

---

### ❷ `makemigrations` を忘れる

**症状**
`models.py` を変更したのにデータベースに反映されない。

**解決方法**
```powershell
python manage.py makemigrations
python manage.py migrate
```

モデルを変更したら必ずこの2つを実行する！

---

### ❸ `INSTALLED_APPS` にアプリを追加し忘れる

**症状**
作ったアプリが認識されない。

**解決方法**
`settings.py` の `INSTALLED_APPS` にアプリ名を追加する。

```python
INSTALLED_APPS = [
    ...
    'plants',  # 追加！
]
```

---

### ❹ フォームに `{% csrf_token %}` を書き忘れる

**症状**
フォームを送信すると `403 Forbidden` エラーになる。

**解決方法**
フォームタグの中に必ず書く。

```html
<form method="post">
  {% csrf_token %}  ← 必須！
  ...
</form>
```

---

### ❺ Renderの `Root Directory` にスペースが入る

**症状**
```
Root directory "yasai_app " does not exist.
```

**解決方法**
Renderの `Settings` で `Root Directory` のスペースを削除する。

`yasai_app ` → `yasai_app`

---

### ❻ `requirements.txt` に `gunicorn` が入っていない

**症状**
```
bash: line 1: gunicorn: command not found
```

**解決方法**
`requirements.txt` に手動で追加する。

```
gunicorn==23.0.0
whitenoise==6.9.0
dj-database-url==2.3.0
```

---

### ❼ サーバーを再起動しないと変更が反映されない

**症状**
コードを変更したのにブラウザに反映されない。

**解決方法**
PowerShellで `Ctrl+C` でサーバーを止めて再起動する。

```powershell
python manage.py runserver
```