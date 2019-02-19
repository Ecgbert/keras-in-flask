# keras-in-flask
deploy keras model in flask

此專案使用ResNet50模型以及Gradient-weighted Class Activation Mapping class activation map(Grad-CAM)視覺化，顯示目標影像對最終分類結果影響最大的區域
這個方法很有趣的地方在於模型在訓練時並沒有使用定位的資訊，單單只有分類的標籤，然而透過Grad-CAM技術能夠發現模型能在不使用定位資訊的情況下隱含的學習到物件的空間資訊，這代表CAM技術除了能夠幫助我們理解網路之外，未來或許能使弱監督技術發展的可能，減少對於人工標記資料的依賴，減少訓練網路的成本

DEMO

![image](https://github.com/lisssse14/keras-in-flask/blob/master/gif.gif)
