# README.md

# 食材検出AIモデル (Ingredient Detector)

このプロジェクトは、YOLOv5をファインチューニングして作成した、特定の食材（じゃがいも、たまねぎ、肉など）を画像から検出するためのAIモデルです。

## 主な機能

- 画像内の食材を検出し、その名前をリストとして出力します。
- 現在検出できる食材: `potato`, `onion`, `meat`, `carrot`
- コマンドラインから簡単に実行できます。

## フォルダ構成
```
curry-ingredient-detector/
│
├── yolov5/                    # 学習済みモデルやYOLOv5のプログラム本体
│   └── runs/train/direct_test_run/weights/
│       └── best.pt            # 学習済みモデル
│
├── datasets/                  # データセット（リポジトリには含まない）
├── curry/                     # (データセットのサンプル)
├── test_images/               # テスト用画像（リポジトリには含まない）
│
├── estimate.py                # 推定実行スクリプト
├── train.py                   # 再学習用スクリプト
├── requirements.txt           # 必要なライブラリ
└── README.md                  
```

## セットアップ方法

1.  **このリポジトリをクローンします:**
```bash
git clone [URL]
cd curry-ingredient-detector
```

2.  **YOLOv5公式リポジトリをクローンします:**
```bash
git clone https://github.com/ultralytics/yolov5.git
```

3.  **仮想環境を作成し、ライブラリをインストールします:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # Mac/Linux
    # venv\Scripts\activate    # Windows
    pip install -r requirements.txt
    ```

## 使い方

以下のコマンドで、画像内の食材を推定し、結果を標準出力に表示します。

```bash
python estimate.py [画像ファイルのパス]
```

## モデルの再学習について

データセットを更新し、モデルを再学習させたい場合は~~`yolov5/train.py`~~ train.pyを使用します。
~~（yolov5フォルダに移動）~~
```bash
# 基本的な再学習コマンド
# 結果は yolov5/runs/train/new_ingredient_model/ に保存されます
python train.py --img 640 --batch 8 --epochs 100 --data ../datasets/data.yaml --weights yolov5s.pt --name new_ingredient_model
```

---

### 書き換える箇所の説明

1.  **`検出可能な食材:`**
    *   Roboflowで設定したクラス名（`potato`, `onion`, `meat`など）をここにリストアップします。

2.  **`yolov5/runs/train/【direct_test_run】/weights/best.pt`**
    *   `【direct_test_run】`の部分を、学習済みモデルが実際に格納されているフォルダ名に書き換えます。　

3.  **`git clone 【...】`**
    *   GitHubでリポジトリを作成した後に払い出される、あなた専用のURLに書き換えます。

4.  **`cd 【リポジトリ名】`**
    *   リポジトリ名（例: `curry-ingredient-detector`）に書き換えます。

5.  **`python estimate.py test_images/images/【サンプル画像のファイル名.jpg】`**
    *   `test_images/images`フォルダの中に、使い方を示すのに最適なサンプル画像があれば、そのファイル名に書き換えます。