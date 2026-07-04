# 食材検出AIモデル (Ingredient Detector)

このプロジェクトは、YOLOv5をファインチューニングして作成した、特定の食材（じゃがいも、たまねぎ、肉、人参）を画像から検出するAIモデルです。

## 主な機能

- 画像内の食材を検出し、その名前をリストとして出力します。
- 現在検出できる食材: `potato`, `onion`, `meat`, `carrot`
- コマンドラインから簡単に実行できます。

## モデルについて

- ベースモデル: YOLOv5s
- 200エポック学習（`yolov5/runs/train/a-better-model/`）
- 検証データでの精度: mAP@0.5 ≈ 0.84、mAP@0.5:0.95 ≈ 0.69

## フォルダ構成
```
curry-ingredient-detector/
│
├── yolov5/                    # YOLOv5本体（別途clone、下記セットアップ参照）
│   └── runs/train/a-better-model/weights/
│       └── best.pt            # 学習済みモデル（本リポジトリに含む）
│
├── datasets/                  # データセット（リポジトリには含まない）
├── curry/                     # (データセットのサンプル、リポジトリには含まない)
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
git clone https://github.com/KannoKens/curry-ingredient-detector.git
cd curry-ingredient-detector
```

2.  **YOLOv5公式リポジトリをクローンします:**
```bash
git clone https://github.com/ultralytics/yolov5.git
```
（学習済みモデル本体 `yolov5/runs/train/a-better-model/weights/best.pt` は本リポジトリに含まれているので、上書きされないよう注意してください。）

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

データセットを更新し、モデルを再学習させたい場合は `train.py` を使用します。

```bash
# 基本的な再学習コマンド
# 結果は yolov5/runs/train/new_ingredient_model/ に保存されます
python train.py --img 640 --batch 8 --epochs 100 --data ../datasets/data.yaml --weights yolov5s.pt --name new_ingredient_model
```
