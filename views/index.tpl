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
        <table class="table table-striped" style="table-layout:fixed;">
            <thead>
            <tr>
                <th style="width:50px;">id</th>
                <th style="width:50px;">OSS</th>
                <th style="width:100px;">Module</th>
                <th style="width:500px;">msgid</th>
                <th style="width:500px;">msgstr</th>
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