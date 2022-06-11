if [ -d "./build" ]
then

    if [ "$(ls -A './build')" ]; then
      echo "Directory 'build' already exists and not empty. Are you sure to remove all its content? y/n: "
      read ans
      if [ $ans = "y" ]
      then
        rm ./build/* -r
      else
        exit 0
      fi
    else
      echo "Directory is Empty. "
    fi
else
    mkdir build
    echo "Directory 'build' created. "
fi

cp GameState.py ./build/GameState.py
cp client_console_graph.py ./build/client_console_graph.py
cp server.py ./build/server.py
cd ./build
pyinstaller -F client_console_graph.py -n client.exe --paths "C:\Python310\Lib\site-packages" --hiddenimport websockets --hiddenimport websockets.legacy --hiddenimport websockets.legacy.client
pyinstaller -F server.py -n server.exe --paths "C:\Python310\Lib\site-packages" --hiddenimport websockets --hiddenimport websockets.legacy --hiddenimport websockets.legacy.server

echo "Enter for exit"
read for_exit
