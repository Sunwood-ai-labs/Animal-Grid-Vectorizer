import os
import sys
from app.app import create_interface



if __name__ == "__main__":
    # アプリケーションのルートディレクトリをPythonパスに追加
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    
    # Gradioインターフェースを作成
    app = create_interface()
    
    # アプリケーションを起動
    app.launch(share=False)
    
    print("アプリケーションを終了しました。")
