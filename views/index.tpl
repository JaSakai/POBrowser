% rebase('base.tpl')

<div class="row">

% include('form.tpl')

</div>

% if len(polist) >= 500:
  <br />
  <div class="alert alert-warning" role="alert">検索結果が500行を超えています。検索語を絞ってください。</div>
% end

<div class="row">
    <div class="table-responsive">
        <table class="table table-striped">
            <thead>
            <tr>
                <th>id</th>
                <th>OSS</th>
                <th>Module</th>
                <th>msgid</th>
                <th>msgstr</th>
            </tr>
            </thead>
            <tbody>

            % for po in polist[0:500]:
              <tr>
                  <td>{{po.id}}</td>
                  <td>{{po.oss}}</td>
                  <td>{{po.module}}</td>
                  <td>{{!po.msgid}}</td>
                  <td>{{!po.msgstr}}</td>
              </tr>
            % end
            </tbody>
        </table>
    </div>
</div>