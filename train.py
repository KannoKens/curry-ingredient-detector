# train.py

import argparse
import os
import subprocess
import sys
from pathlib import Path

# --- 設定項目 ---
# データセット設定ファイルのパス (プロジェクトルートからの相対パス)
DATA_YAML_PATH = 'datasets/data.yaml'

def train_model(args):
    """
    YOLOv5の学習スクリプトをサブプロセスとして実行する関数。
    """
    # yolov5フォルダのパスを解決
    yolov5_dir = Path('yolov5')
    if not yolov5_dir.is_dir():
        print(f"エラー: 'yolov5' フォルダが見つかりません。")
        print("カレントディレクトリがプロジェクトのルートフォルダであることを確認してください。")
        return

    # YOLOv5のtrain.pyのパス
    data_path_for_yolo = os.path.relpath(DATA_YAML_PATH, str(yolov5_dir))

    # 学習コマンドを組み立てる
    command = [
        sys.executable,
        'train.py',  #修正点1: パスを単純なファイル名に変更
        '--img', str(args.img_size),
        '--batch', str(args.batch_size),
        '--epochs', str(args.epochs),
        '--data', data_path_for_yolo, # 修正点2: 変換後のパスを使用
        '--weights', args.weights,
        '--name', args.name,
        '--cache'
    ]
    
    # --deviceが指定されていればコマンドに追加
    if args.device:
        command.extend(['--device', args.device])

    print("以下のコマンドで学習を開始します:")
    print(' '.join(command))
    print("-" * 30)

    # サブプロセスとして学習を実行
    # cwd=yolov5_dir を指定することで、yolov5フォルダ内でコマンドが実行される
    try:
        subprocess.run(command, check=True, cwd=yolov5_dir)
        print("-" * 30)
        print("学習が正常に完了しました。")
        print(f"学習済みモデルは 'yolov5/runs/train/{args.name}/' に保存されています。")
    except subprocess.CalledProcessError as e:
        print("-" * 30)
        print(f"学習中にエラーが発生しました: {e}")
    except KeyboardInterrupt:
        print("\n学習がユーザーによって中断されました。")


def main():
    """
    メインの実行関数。コマンドラインから引数を受け取る。
    """
    parser = argparse.ArgumentParser(description='YOLOv5モデルの学習を行います。')
    
    # 学習パラメータの設定
    parser.add_argument('--epochs', type=int, default=100, help='学習のエポック数')
    parser.add_argument('--batch-size', type=int, default=8, help='バッチサイズ (PCのVRAMに応じて調整)')
    parser.add_argument('--img-size', type=int, default=640, help='入力画像のサイズ')
    parser.add_argument('--weights', type=str, default='yolov5s.pt', help='初期重みファイル (例: yolov5s.pt, yolov5m.pt)')
    parser.add_argument('--name', type=str, default='local_training_run', help='学習結果を保存するフォルダ名')
    parser.add_argument('--device', type=str, default=None, help='使用するデバイス (例: 0 or cpu)')
    
    args = parser.parse_args()

    train_model(args)

if __name__ == '__main__':
    main()