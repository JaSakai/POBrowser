% rebase('base.tpl')

<div class="jumbotron">
<h1 class='page-header'>PO Browser</h1>
<p>大学教育に利用される各種OSSの翻訳をキーワード検索します。</p>
</div>
<p>次の入力域に検索語を入力してください。</p>

% include('form.tpl')

<br>
<br>
<br>

<div class="row">
<div class="col-xs-12">
<p></p>
	<ul class="nav nav-tabs">
	  <li class="active"><a href="#1" data-toggle="tab">利用方法</a></li>
	  <li><a href="#2" data-toggle="tab">What is POBrowser?</a></li>
	  <li><a href="#3" data-toggle="tab">データソース</a></li>
	</ul>
	<div class="tab-content">
	  <div class="tab-pane active" id="1">
	  <br>
	  <ul>
	    <li>検索語として英語および日本語が使えます。</li>
	    <li>複数の検索語を使う場合には区切り文字として半角スペースを使います。</li>
	    <li>検索語の先頭に = をつけると、その検索語だけを含む文字列を検索します。</li>
	    <li>検索語の先頭に ! をつけると、その検索語を含まない文字列を検索します。</li>	    
	    <li>英語は Case Insensitevieですので、小文字、大文字でも同じ結果となります。<br>
	    例1：英語の検索語をgradeおよびaddとし、日本語では成績を含み、方略は含まない検索の場合<br>
	    　Search Term:　 grade　add、 検索語：　成績　!方略<br>
	    例2：英単語のみの検索の場合<br>
	    　Search Term:　 =grade</li>
	    <li>検索対象のPOはSakaiが初期値ですが、Moodle、MaharaのPOも対象とする場合にはチェックボックスをクリックします。</li>
	    <li>検索結果表示画面からこの画面に戻るには、右上に表示される[TOPページ]ボタンをクリックします。</li>
	  </ul>
	  </div>
	  <div class="tab-pane" id="2">
	  <br>
	    <ul>
	    <li>大学教育で利用されるシステムの翻訳結果を横断的にまとめた事例ベースの文字列単位の用例集です。</li>
	    <li>それぞれのシステムもしくはモジュール単位で使われる用語を検索できます。</li>
	    <li>一つの用語に対してそれぞれのシステムにおける翻訳を参照できます。</li>
	    <li>それぞれのシステムの翻訳結果をPOファイルに変換して、それをデータベース化しています。</li>
	    <li>2012-2014年度の科研費における研究成果です。
		</ul>
	  </div>	  
	  <div class="tab-pane" id="3">
	  <br>
	    <ul>
	    <li>PO出典</li>
			<ul>
		    <li>Sakai trunk (最新版)</li>
		    <li>Moodle 2.6.1</li>
		    <li>Mahara 1.8.1</li>
		  　</ul>
		 <li>Acknowledgement</li>
		 	<ul>
		 	<li>Transifex</li>
		 	<li>関根裕紀、入門Webアプリケーション開発、Pythonエンジニア養成読本、Software Design plus、技術評論社、2015、東京</li>
		 	</ul>
		</ul>
	  </div>
	</div>
</div>
</div>