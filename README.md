# ainews.komee.org — 生成AIニュースまとめ

GitHub Actions で毎日 RSS を取得して静的 HTML を生成し、GitHub Pages で公開する自動ブログ。

## 使い方（最短）
1. このリポジトリを GitHub に作成し、ブランチ `main` へ push
2. Settings → Pages → Source: `Deploy from branch`, Branch: `main`, Folder: `/docs`
3. `docs/CNAME` に独自ドメイン `ainews.komee.org` を設定（DNS で CNAME も設定）
4. Actions → `build-ai-news` を手動で Run（初回生成）

## 構成
- `data/feeds.json` : RSS リスト
- `scripts/build_news.py` : 収集して `/docs/index.html` と `/docs/news/YYYY-MM-DD.html` を生成
- `templates/*.j2` : Jinja2 テンプレート（AdSense スロットは適宜変更）

## 依存
- feedparser
- jinja2

## ライセンス
MIT
