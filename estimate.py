import torch
import argparse
import os
import sys
from pathlib import Path

# ----------------------------------------------------
# 設定項目 (実行前にここを確認・変更)
# ----------------------------------------------------
# 学習済みモデルが保存されている「実行名」フォルダ
#    (例: 'direct_test_run', 'my_final_model' など)
RUN_NAME = 'direct_test_run'

# 検出の信頼度のデフォルトしきい値 (0.0 ~ 1.0)
DEFAULT_CONFIDENCE = 0.4
# ----------------------------------------------------


def estimate_ingredients(image_path, model, confidence_threshold):
    """
    画像ファイルへのパスを受け取り、写っている材料名のリストを返す関数。
    """
    try:
        results = model(image_path)
        detections_df = results.pandas().xyxy[0]
        ingredient_list = detections_df[detections_df['confidence'] > confidence_threshold]['name'].unique().tolist()
        return ingredient_list
    except Exception as e:
        # 画像の読み込み失敗など、予期せぬエラーに対応
        print(f"エラー: 画像の解析中に問題が発生しました。ファイルが破損している可能性があります。 ({e})", file=sys.stderr)
        return None

def load_model(run_name):
    """
    指定された実行名の学習済みモデルを読み込む関数。
    """
    yolov5_dir = Path('yolov5')
    if not yolov5_dir.is_dir():
        print("エラー: 'yolov5' フォルダが見つかりません。", file=sys.stderr)
        return None

    model_path = yolov5_dir / 'runs/train' / run_name / 'weights/best.pt'
    if not model_path.is_file():
        print(f"エラー: モデルファイルが見つかりません。パスを確認してください: {model_path}", file=sys.stderr)
        return None

    try:
        model = torch.hub.load(
            str(yolov5_dir),
            'custom',
            path=model_path,
            source='local',
            verbose=False # torch.hubのログを非表示にする
        )
        return model
    except Exception as e:
        print(f"エラー: モデルの読み込み中に問題が発生しました: {e}", file=sys.stderr)
        return None

def main():
    """
    メインの実行関数。
    """
    parser = argparse.ArgumentParser(description='画像から材料名を推定し、リストとして出力します。')
    parser.add_argument('image_path', type=str, help='解析したい画像ファイルのパス')
    parser.add_argument('--conf', type=float, default=DEFAULT_CONFIDENCE, help=f'検出の信頼度のしきい値 (デフォルト: {DEFAULT_CONFIDENCE})')
    args = parser.parse_args()

    # 画像ファイルの存在チェック
    if not os.path.exists(args.image_path):
        print(f"エラー: 画像ファイルが見つかりません: {args.image_path}", file=sys.stderr)
        sys.exit(1) # エラーでプログラムを終了

    # モデルを読み込む
    model = load_model(RUN_NAME)
    if model is None:
        sys.exit(1) # モデル読み込み失敗で終了

    # 材料を推定する
    estimated_list = estimate_ingredients(args.image_path, model, args.conf)

    # 結果を出力する
    if estimated_list is not None:
        # 推定された材料が一つでもあれば、それらを改行区切りで出力
        if estimated_list:
            for ingredient in estimated_list:
                print(ingredient)
        # 何も見つからなかった場合は何も出力しない (サイレント)
        # else:
        #     pass 

if __name__ == '__main__':
    main()