# Python 入門ガイド

## 目次
1. [Pythonとは？](#pythonとは)
2. [基本用語](#基本用語)
3. [変数と型](#変数と型)
4. [文字列の操作](#文字列の操作)
5. [リスト](#リスト)
6. [辞書](#辞書)
7. [for文](#for文)
8. [if文](#if文)
9. [関数](#関数)
10. [RubyとPythonの比較](#rubyとpythonの比較)

---

## Pythonとは？

PythonはシンプルなコードでAI・Web開発・データ分析など幅広い用途に使えるプログラミング言語です。

**特徴**
- コードがシンプルで読みやすい
- インデント（字下げ）でコードのまとまりを表す
- ライブラリが豊富でAI・データ分析・Web開発に強い

---

## 基本用語

| 用語 | 意味 |
|------|------|
| 変数 | データを入れる箱 |
| 型 | データの種類（文字・数値・真偽値など） |
| リスト | 複数のデータをまとめる配列 |
| 辞書 | キーと値のペアでデータをまとめるもの |
| 関数 | 処理をまとめて名前をつけたもの |
| インデント | コードの字下げ。Pythonではコードのまとまりを表す |
| pip | Pythonのパッケージ管理ツール（npmのようなもの） |

---

## 変数と型

Pythonは型宣言が不要です。値を代入すると自動的に型が決まります。

```python
# 文字列（str）
name = "愛梨"

# 整数（int）
age = 22

# 小数（float）
height = 1.58

# 真偽値（bool）
is_student = True

# 型を確認したいとき
print(type(name))    # → <class 'str'>
print(type(age))     # → <class 'int'>
print(type(height))  # → <class 'float'>
print(type(is_student)) # → <class 'bool'>
```

**ポイント**
- JavaやTypeScriptと違い型を書かなくていい
- Rubyと同じ感覚で使える

---

## 文字列の操作

### fstring（エフストリング）

文字列の前に `f` をつけると `{}` の中に変数を埋め込めます。

```python
name = "愛梨"
age = 22
height = 1.58

# fstringを使った書き方（おすすめ）
print(f"名前：{name}、年齢：{age}歳、身長：{height}m")
# → 名前：愛梨、年齢：22歳、身長：1.58m

# 昔の書き方（面倒）
print("名前：" + name + "、年齢：" + str(age) + "歳")
```

---

## リスト

複数のデータをまとめる配列です。Rubyの配列と同じ概念です。

```python
# リストの作成
vegetables = ["トマト", "きゅうり", "なす", "ピーマン"]

print(vegetables)        # → ['トマト', 'きゅうり', 'なす', 'ピーマン']
print(vegetables[0])     # → トマト（0番目から始まる）
print(vegetables[-1])    # → ピーマン（最後の要素）
print(len(vegetables))   # → 4（要素の数）

# 要素の追加
vegetables.append("かぼちゃ")
print(vegetables)  # → ['トマト', 'きゅうり', 'なす', 'ピーマン', 'かぼちゃ']

# 要素の削除
vegetables.remove("なす")
print(vegetables)  # → ['トマト', 'きゅうり', 'ピーマン', 'かぼちゃ']
```

**RubyとPythonの比較**
```ruby
# Ruby
vegetables = ["トマト", "きゅうり"]
vegetables.push("なす")
```
```python
# Python
vegetables = ["トマト", "きゅうり"]
vegetables.append("なす")
```

---

## 辞書

キーと値のペアでデータをまとめるものです。Rubyのハッシュと同じ概念です。

```python
# 辞書の作成
tomato = {
    "name": "トマト",
    "season": "夏",
    "days": 90,  # 収穫までの日数
}

print(tomato)              # → {'name': 'トマト', 'season': '夏', 'days': 90}
print(tomato["name"])      # → トマト（キーで値を取得）
print(tomato["season"])    # → 夏

# 値の追加・更新
tomato["color"] = "赤"
print(tomato)  # → {'name': 'トマト', 'season': '夏', 'days': 90, 'color': '赤'}
```

**RubyとPythonの比較**
```ruby
# Ruby（シンボルをキーに使う）
tomato = { name: "トマト", season: "夏" }
tomato[:name]  # → "トマト"
```
```python
# Python（文字列をキーに使う）
tomato = { "name": "トマト", "season": "夏" }
tomato["name"]  # → "トマト"
```

---

## for文

リストの中身を一個ずつ取り出して処理します。

```python
vegetables = ["トマト", "きゅうり", "なす", "ピーマン"]

# 基本のfor文
for vegetable in vegetables:
    print(f"{vegetable}を育てています")
# → トマトを育てています
# → きゅうりを育てています
# → なすを育てています
# → ピーマンを育てています

# インデックスも取得したいとき
for i, vegetable in enumerate(vegetables):
    print(f"{i+1}番目：{vegetable}")
# → 1番目：トマト
# → 2番目：きゅうり
```

**⚠️ Pythonのfor文の重要なポイント**

Pythonはインデント（字下げ）でコードのまとまりを表します。
`end` は不要ですが、インデントがずれるとエラーになります！

```python
# 正しい書き方
for vegetable in vegetables:
    print(vegetable)   # インデントあり → forの中
    print("育ててます") # インデントあり → forの中

print("終わり") # インデントなし → forの外

# 間違った書き方（エラーになる）
for vegetable in vegetables:
print(vegetable)  # インデントなし → エラー！
```

**RubyとPythonの比較**
```ruby
# Ruby（endが必要）
vegetables.each do |vegetable|
  puts "#{vegetable}を育てています"
end
```
```python
# Python（endは不要、インデントで管理）
for vegetable in vegetables:
    print(f"{vegetable}を育てています")
```

---

## if文

条件によって処理を分岐します。

```python
age = 22

if age >= 20:
    print("成人です")
elif age >= 13:
    print("中高生です")
else:
    print("子供です")
# → 成人です
```

**ポイント**
- `elif` はRubyの `elsif` と同じ
- `:` を忘れずに書く
- インデントで処理のまとまりを表す

---

## 関数

処理をまとめて名前をつけたものです。

```python
# 基本の関数
def plant_info(name, days):
    print(f"{name}は種まきから{days}日で収穫できます")

plant_info("トマト", 90)    # → トマトは種まきから90日で収穫できます
plant_info("きゅうり", 60)  # → きゅうりは種まきから60日で収穫できます

# 戻り値のある関数
def calc_harvest_month(sow_month, days):
    harvest_month = sow_month + (days // 30)
    return harvest_month

result = calc_harvest_month(4, 90)
print(f"収穫月：{result}月")  # → 収穫月：7月
```

**関数の構造**
```python
def 関数名(引数1, 引数2):
    # 処理
    return 戻り値  # 戻り値がない場合は省略可
```

**RubyとPythonの比較**
```ruby
# Ruby
def plant_info(name, days)
  puts "#{name}は#{days}日で収穫できます"
end
```
```python
# Python
def plant_info(name, days):
    print(f"{name}は{days}日で収穫できます")
```

---

## RubyとPythonの比較

| 機能 | Ruby | Python |
|------|------|--------|
| 文字列の埋め込み | `"#{name}"` | `f"{name}"` |
| 配列・リスト | `array = []` | `list = []` |
| ハッシュ・辞書 | `{ key: value }` | `{ "key": value }` |
| キーの種類 | シンボル（`:name`） | 文字列（`"name"`） |
| 繰り返し | `each do \|x\|...end` | `for x in list:` |
| 関数定義 | `def name...end` | `def name():` |
| 出力 | `puts` | `print()` |
| ブロックの終わり | `end` | インデント |
| 展開 | `*array` | `*array` |