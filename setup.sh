#!/bin/bash

# 設定 Image 名稱
IMAGE_NAME="streamlit-app"

# 檢查是否已存在該 Image，若有則刪除
if [[ "$(docker images -q $IMAGE_NAME 2> /dev/null)" != "" ]]; then
    echo "⚠️ 檢測到已存在的 Image：$IMAGE_NAME，刪除中..."
    docker rmi -f $IMAGE_NAME
    echo "✅ 已刪除 $IMAGE_NAME"
fi

# 重新建置 Docker Image
echo "🚀 開始建置 Docker Image：$IMAGE_NAME"
docker build -t $IMAGE_NAME .

echo "✅ 建置完成！"
