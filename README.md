# POBrowser
大学教育用OSSを翻譯して生成されるPOをOSSを横断して検索するシステムです。
ソースコードに含まれるOSSのPOはSakai, Moodle, Maharaです。
#### システム概要
Pythonにて開発しました。理由としてはgettext POファイルをためのPOLIBが利用できたためです。PHPでは同等のモジュールを見つけることができませんでした。
フレームワークとしてBottle, SLQAlchemy, WTFormsを使っています。

#### Contents
データベースにPOをインポートするPOImporterとそれらを検索するPOBrowserから構成されます。

###### POBrowser
* pobrowser.py: データベースを各種条件にて検索するためのメインプログラムです。
* views/*.tpl：PythonフレームワークBottle用テンプレートです。
* pobrowser.conf: MySQL関連設定などを記載します。

###### POImporter
* poimporter.py: POファイルをデータベースにインポートするメインプロログラムです。
* pos/{oss名}/*.po: データベースにインポートされるPOファイルです。
* DB_setting_example.txt: データベース環境構築事例です。

#### Pre-Requisite
下記、いずれの環境でも稼働実績があります。
* AWS LINUX amzn-ami-hvm-2016.03.2.x86_64-gp2 (ami-6154bb00)
* OSX Yosemite (10.10.5))

######yumにて導入(Amazon LINUX)
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

#### 環境設定および実行
1. 実行環境を構築します。
2. git clone にてPOBrowserのソースコード(ワークツリー)をダウンロードします。
3. MySQLにmysqlでアクセスし、DB_setting_example.txtを参考にしてデータベースおよびユーザを設定します。
4. POBrowserディレクトリにて python poimporter.py を実行します。これによりデータペースにテーブルが作成されます。データベース名、ユーザ名などを変更するには、pobrowser.confを変更してください。
5. POBrowserディレクトリにて python pobrowser.py を実行します。ブラウザにてlocalhost:8080/pobrowser でアクセスします。


