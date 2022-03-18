# Excel文件轉Rpy腳本 （Key版）

## 開發環境
- Python 3.8

## 模塊劃分
```
|
|-corelib 基礎依賴
     |-- exception  自定義的異常
|-dist 打包的exe文檔
|-handler
     |-- converter  將Excel中的數據轉化為rpy中的對象
     |-- render     將model中的元素與進程控制渲染成Rpy腳本文檔
|-model
     |-- element Rpy遊戲的基本元素
     |-- process Rpy遊戲的進程控制
|--tools  工具類
|--app.py 程序入口
```


## 打包程序
- 工具: pyinstaller  
- CMD: `pyinstaller -F -w -i .\asset\sos.ico .\app.py -n Excel2RpyScript`

## relase notes
- 0.1.1
    - fix [立繪回收 #20](https://github.com/HaruhiFanClub/Excel2RpyScript/issues/20)
    - fix [Nvl模式與adv模式的切換 #19](https://github.com/HaruhiFanClub/Excel2RpyScript/issues/19)
    - 去掉Exe文件的外部依賴

- 0.2.4
    - fix 條件選擇在最後一行時無法讀取
    - 支持對話框頭像

- 1.0.0 key版
    - 全局改善Excel結構

- 1.0.1 key版
    - 好感度判定，數值加減
    
- 1.0.2 key版
    - 二週目才能選的選項