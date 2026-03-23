# Django 入門ガイド

## 目次
1. [Djangoとは？](#djangoとは)
2. [MVTとは？](#mvtとは)
3. [models.pyの基本](#modelspyの基本)
4. [views.pyの基本](#viewspyの基本)
5. [urls.pyの基本](#urlspyの基本)
6. [templatesの基本](#templatesの基本)
7. [forms.pyの基本](#formspyの基本)
8. [管理画面の説明](#管理画面の説明)
9. [よく使うコマンド一覧](#よく使うコマンド一覧)

---

## Djangoとは？

DjangoはPythonのWebフレームワークです。
「バッテリー同梱（batteries included）」と呼ばれるほど最初から機能が豊富です。

**特徴**
- 管理画面が自動生成される
- ログイン・認証機能が最初から入っている
- データベース操作が簡単にできる
- セキュリティ対策が最初から入っている

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

## models.pyの基本

`models.py` はデータベースのテーブル設計を書くファイルです。

### 基本の書き方

```python
from django.db import models

class Plant(models.Model):
    # フィールド名 = フィールドの種類(オプション)
    name = models.CharField(max_length=100)        # 短い文字列
    season = models.CharField(max_length=50)       # 短い文字列
    sow_month = models.IntegerField()              # 整数
    harvest_month = models.IntegerField()          # 整数
    days_to_harvest = models.IntegerField()        # 整数
    memo = models.TextField(blank=True)            # 長い文字列（空でもOK）
    created_at = models.DateTimeField(auto_now_add=True)  # 日時（自動）

    def __str__(self):
        return self.name  # 管理画面などで表示する名前
```

### よく使うフィールドの種類

| フィールド | 意味 | 例 |
|-----------|------|----|
| `CharField` | 短い文字列 | 名前・タイトル |
| `TextField` | 長い文字列 | メモ・本文 |
| `IntegerField` | 整数 | 年齢・数量 |
| `FloatField` | 小数 | 価格・身長 |
| `BooleanField` | 真偽値 | フラグ |
| `DateField` | 日付 | 生年月日 |
| `DateTimeField` | 日時 | 作成日時 |
| `ForeignKey` | 外部キー（他のモデルと関連） | ユーザーID |

### よく使うオプション

| オプション | 意味 |
|-----------|------|
| `blank=True` | 空でもOK |
| `null=True` | NULLを許可 |
| `auto_now_add=True` | 作成時の日時を自動で保存 |
| `auto_now=True` | 更新時の日時を自動で保存 |
| `max_length=100` | 最大文字数 |
| `default=0` | デフォルト値 |

### モデルをデータベースに反映する

```powershell
# models.pyの変更をファイルに変換する
python manage.py makemigrations

# データベースに反映する
python manage.py migrate
```

> ⚠️ **models.pyを変更したら必ずこの2つを実行する！**

---

## views.pyの基本

`views.py` は画面に表示する処理を書くファイルです。

### 基本の書き方

```python
from django.shortcuts import render, redirect, get_object_or_404
from .models import Plant
from .forms import PlantForm

# 一覧ページ
def plant_list(request):
    # データベースから全件取得
    plants = Plant.objects.all()
    # テンプレートにデータを渡して表示
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
    # IDでデータ取得（見つからなければ404エラー）
    plant = get_object_or_404(Plant, pk=pk)
    return render(request, 'plants/plant_detail.html', {'plant': plant})

# 削除
def plant_delete(request, pk):
    plant = get_object_or_404(Plant, pk=pk)
    if request.method == 'POST':  # 削除確認後
        plant.delete()            # データベースから削除
        return redirect('plant_list')
    return render(request, 'plants/plant_confirm_delete.html', {'plant': plant})
```

### よく使うデータ取得方法

| コード | 意味 |
|--------|------|
| `Plant.objects.all()` | 全件取得 |
| `Plant.objects.get(pk=1)` | IDで1件取得 |
| `Plant.objects.filter(season='夏')` | 条件で絞り込み |
| `Plant.objects.order_by('name')` | 並び替え |
| `Plant.objects.count()` | 件数を取得 |
| `get_object_or_404(Plant, pk=pk)` | IDで取得（なければ404） |

### renderとredirectの違い

| 関数 | 意味 | 使う場面 |
|------|------|---------|
| `render` | テンプレートを表示する | ページを表示するとき |
| `redirect` | 別のURLに移動する | 保存・削除後にページ移動するとき |

---

## urls.pyの基本

`urls.py` はURLのルーティング設定を書くファイルです。

### プロジェクト全体のurls.py

```python
# yasai_app/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),      # 管理画面
    path('', include('plants.urls')),     # plantsアプリのURLに任せる
]
```

### アプリのurls.py

```python
# plants/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.plant_list, name='plant_list'),                     # 一覧
    path('create/', views.plant_create, name='plant_create'),          # 追加
    path('detail/<int:pk>/', views.plant_detail, name='plant_detail'), # 詳細
    path('delete/<int:pk>/', views.plant_delete, name='plant_delete'), # 削除
]
```

### pathの書き方

```python
path('URL/', views.関数名, name='URL名')
```

| 部分 | 意味 |
|------|------|
| `'URL/'` | アクセスするURL |
| `views.関数名` | 実行するview関数 |
| `name='URL名'` | テンプレートから参照するための名前 |

### URLに値を埋め込む

```python
# <int:pk> でURLの中に数字を埋め込める
path('detail/<int:pk>/', views.plant_detail, name='plant_detail')

# アクセス例
# http://127.0.0.1:8000/detail/1/ → pk=1
# http://127.0.0.1:8000/detail/2/ → pk=2
```

| 書き方 | 意味 |
|--------|------|
| `<int:pk>` | 整数 |
| `<str:name>` | 文字列 |
| `<slug:slug>` | スラッグ（英数字とハイフン） |

---

## templatesの基本

テンプレートはブラウザに表示するHTMLファイルです。
Djangoのテンプレート記法を使ってデータを表示できます。

### テンプレートの置き場所

```
アプリ名/
└── templates/
    └── アプリ名/
        └── *.html
```

### よく使うテンプレート記法

| 記法 | 意味 |
|------|------|
| `{{ 変数名 }}` | 変数を表示する |
| `{{ 変数名\|フィルター }}` | フィルターを適用して表示する |
| `{% for x in list %}` | forループ |
| `{% endfor %}` | forループの終わり |
| `{% if 条件 %}` | 条件分岐 |
| `{% elif 条件 %}` | 条件分岐（else if） |
| `{% else %}` | 条件分岐（else） |
| `{% endif %}` | ifの終わり |
| `{% url 'URL名' %}` | URL名からURLを生成 |
| `{% url 'URL名' pk %}` | URLに値を渡す |
| `{% csrf_token %}` | セキュリティ対策（フォームに必須） |

### 使用例

```html
<!-- 変数を表示 -->
<h1>{{ plant.name }}</h1>

<!-- フィルターで日付をフォーマット -->
<p>{{ plant.created_at|date:"Y年m月d日" }}</p>

<!-- forループ -->
{% for plant in plants %}
  <p>{{ plant.name }}</p>
{% endfor %}

<!-- if文 -->
{% if plant.memo %}
  <p>{{ plant.memo }}</p>
{% else %}
  <p>メモなし</p>
{% endif %}

<!-- URLを生成 -->
<a href="{% url 'plant_list' %}">一覧へ</a>
<a href="{% url 'plant_detail' plant.pk %}">詳細へ</a>

<!-- フォーム -->
<form method="post">
  {% csrf_token %}
  {{ form.as_p }}
  <button type="submit">保存</button>
</form>
```

### よく使うフィルター

| フィルター | 意味 | 例 |
|-----------|------|----|
| `date:"Y年m月d日"` | 日付をフォーマット | `2026年03月21日` |
| `length` | 文字数・件数を取得 | `{{ plants\|length }}` |
| `upper` | 大文字にする | `{{ name\|upper }}` |
| `lower` | 小文字にする | `{{ name\|lower }}` |
| `default:"なし"` | 値がない場合のデフォルト | `{{ memo\|default:"なし" }}` |

---

## forms.pyの基本

`forms.py` はフォームの設定を書くファイルです。

### ModelFormの書き方

`ModelForm` を使うとモデルからフォームを自動生成できます。

```python
from django import forms
from .models import Plant

class PlantForm(forms.ModelForm):
    class Meta:
        model = Plant   # どのモデルを使うか
        fields = ['name', 'season', 'memo']  # 表示する項目
        labels = {
            'name': '野菜名',    # 項目名を日本語に
            'season': '季節',
            'memo': 'メモ',
        }
        widgets = {
            # 入力欄のデザインをカスタマイズ
            'name': forms.TextInput(attrs={
                'class': 'form-control',       # Bootstrapのクラス
                'placeholder': '例：トマト',   # プレースホルダー
            }),
            'memo': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,  # テキストエリアの高さ
            }),
        }
```

### Metaクラスに書けるもの

| キーワード | 意味 |
|-----------|------|
| `model` | どのモデルを使うか |
| `fields` | 表示する項目を指定 |
| `exclude` | 除外する項目を指定 |
| `labels` | 項目名を変える |
| `widgets` | 入力欄のデザインを変える |
| `help_texts` | 入力欄の下にヒント文を表示する |

### よく使うWidget

| Widget | 意味 |
|--------|------|
| `forms.TextInput` | 1行テキスト入力 |
| `forms.Textarea` | 複数行テキスト入力 |
| `forms.NumberInput` | 数値入力 |
| `forms.Select` | ドロップダウン |
| `forms.CheckboxInput` | チェックボックス |
| `forms.DateInput` | 日付入力 |

### attrsに書けるもの

`attrs` にはHTMLの属性をそのまま書けます。

```python
forms.TextInput(attrs={
    'class': 'form-control',          # CSSクラス
    'style': 'border-radius: 10px;',  # インラインスタイル
    'placeholder': '入力してください', # プレースホルダー
    'id': 'my-input',                 # ID
    'required': True,                 # 必須入力
})
```

---

## 管理画面の説明

Djangoには最初から管理画面が用意されています。
`admin.py` に1行書くだけで使えます。

### 管理画面を使えるようにする

```python
# plants/admin.py
from django.contrib import admin
from .models import Plant

admin.site.register(Plant)  # 管理画面にPlantを登録
```

### スーパーユーザーを作成する

```powershell
python manage.py createsuperuser
```

ユーザー名・メールアドレス・パスワードを入力します。

### 管理画面にアクセスする

`http://127.0.0.1:8000/admin/` を開いてログインします。

### 管理画面でできること

| 機能 | 説明 |
|------|------|
| データの一覧表示 | 登録されているデータを一覧で確認 |
| データの追加 | フォームからデータを追加 |
| データの編集 | データを編集 |
| データの削除 | データを削除 |
| ユーザー管理 | ユーザーの追加・編集・削除 |

> 💡 **管理画面は開発者・管理者用のツールです**
> 一般ユーザーには見せないように注意してください。
> 本番環境では強力なパスワードを設定しましょう！

---

## よく使うコマンド一覧

### プロジェクト・アプリ作成

```powershell
# プロジェクト作成
django-admin startproject プロジェクト名

# アプリ作成
python manage.py startapp アプリ名
```

### サーバー起動

```powershell
# 開発サーバー起動
python manage.py runserver

# ポートを指定して起動
python manage.py runserver 8080
```

### データベース

```powershell
# models.pyの変更をファイルに変換
python manage.py makemigrations

# データベースに反映
python manage.py migrate

# 現在のmigrationの状態を確認
python manage.py showmigrations
```

### ユーザー管理

```powershell
# スーパーユーザー作成
python manage.py createsuperuser
```

### その他

```powershell
# Djangoのシェルを起動（データベースを直接操作できる）
python manage.py shell

# 静的ファイルを集める（本番環境用）
python manage.py collectstatic
```