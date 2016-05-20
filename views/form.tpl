
<div class="col-xs-10">
<form class="form-inline text-left" action="/pobrowser/search" method="post">
  <div class="form-group">
      {{ !form.word.label }}
      {{ !form.word(class_="form-control", placeholder=u"英語を入力", maxlength="100") }}

      % if form.word.errors:
          <div class="errors">
          % for error in form.word.errors:
              <p class="text-danger">{{ error }}</p>
          % end
          </div>
      % end

  </div>

  <div class="form-group">
      {{ !form.jword.label }}
      {{ !form.jword(class_="form-control", placeholder=u"日本語を入力", maxlength="100") }}

      % if form.jword.errors:
          <div class="errors">
          % for error in form.jword.errors:
              <p class="text-danger">{{ error }}</p>
          % end
          </div>
      % end

  </div>

  <div class="form-group">
      % if request.path == "/pobrowser":
       {{ !form.sakai.label }}
       {{ !form.sakai(class_="form-control", checked=True)}}
      % else:
       {{ !form.sakai.label }}
       {{ !form.sakai(class_="form-control", checked=False)}}
      % end



  </div>
  <div class="form-group">
      {{ !form.moodle.label }}
      {{ !form.moodle(class_="form-control", checked=False)}}

  </div>
  <div class="form-group">
      {{ !form.mahara.label }}
      {{ !form.mahara(class_="form-control", checked=False)}}
  </div>

  <input type="submit" class="btn btn-default" value="検索"/>
</form>
</div>

% if request.path == "/pobrowser/search":
  <div class="col-xs-2">
    <a class="btn btn-info" href="/pobrowser">TOPページ</a>
  </div>
% end
