# POBrowser
大学教育用OSSを翻譯して生成されるPOをOSSを横断して検索するシステムです。
ソースコードに含まれるOSSのPOはSakai, Moodle, Maharaです。
#### Contents
データベースにPOをインポートするPOImporterとそれらを検索するPOBrowserから構成されます。

###### POBrowser
* pobrowser.py: メインプログラムです。
* views/*.tpl：PythonフレームワークBottle用テンプレートです。

###### POImporter
* poimporter.py: メインプロログラムです。
* pos/{oss名}/*.po: データベースにインポートされるPOファイルです。
* 

#### 実行環境 (AWS CentOS 6)

######yumにて導入
* python 2.7.10
* MySQL 5.6.25
* Apache 2.2.31
* PIP 8.1.2
* git  2.7.4
* python-devel  <= MySQL-pythonの前提
* mysql-devel  <= MySQL-pythonの前提
* gcc  <= MySQL-pythonの前提

######pipにて導入
* bottle (0.12.9)
* bottle-sqlalchemy (0.4.3)
* MySQL-python (1.2.5) 
* polib (1.0.7)
* setuptools (18.2)
* SQLAlchemy (1.0.12)
* transifex-client (0.11b3)
* wheel (0.24.0)
* WTForms (2.1)

#### 環境設定
