
var token = sessionStorage.token || localStorage.token;
var user_id = localStorage.user_id;

//获取用户基本信息
function getUserInfo() {
     $.ajax({
         url:host+"/user/"+user_id+"/info/",
         type:"get",
         headers:{
            "Authorization": "JWT " + token
        },
         contentType:"application/json"
    }).done(function (resp) {
        user_info = resp.data;
        $("#profile_url").attr("src",user_info.avatar_url);
        $("#signature").attr("value",user_info.signature);
        $("#nick_name").attr("value",user_info.username);
         if(user_info.gender == 1){
             $("input[name='gender']:eq(0)").prop("checked",true);
             $("input[name='gender']:eq(1)").prop("checked",false);
         }else {
             $("input[name='gender']:eq(1)").prop("checked",true);
             $("input[name='gender']:eq(0)").prop("checked",false);
         }

         }).fail(function (resp) {
            //如果签证token过期刷新页面
             if(resp.status==401){
                 location.reload();
            parent.location.reload();
             }
             alert(resp.errmsg);
        });
}


//预览头像
function uploadImg(element, tag) {
        var file = tag.files[0];
        var imgSrc;
        if (!/image\/\w+/.test(file.type)) {
            alert("看清楚，这个需要图片！");
            return false;
        }
        var reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = function() {
            console.log(this.result);
            imgSrc = this.result;
            element.attr("src", imgSrc);
        };
    }

//上传头像
function UserImg() {
    $(".upload_aval").submit(function (e) {
        e.preventDefault();
        if(!$("#user_img").val()){
            // 数据为空
            return;
        }

        //TODO 上传头像
        // 上传头像,表单提交和其他提交方式不一样

        $(this).ajaxSubmit({
            url: host+"/user/"+user_id+"/avatar/",
            type: "put",
            headers: {
                "Authorization": "JWT " + token
            }
        }).done(function (resp){
                    sessionStorage.avatar_url = resp.avatar_url;
                    localStorage.avatar_url = resp.avatar_url;
                    //提示信息
                    alert(resp.errmsg);
                    //更新界面
                    $(".now_user_pic").attr("src", resp.avatar_url);
                    $(".user_center_pic>img", parent.document).attr("src", resp.avatar_url);
                    $(".info_icon", parent.document).attr("src", resp.avatar_url);
                    parent.location.reload();
                })
        .fail(function (resp) {
            //如果签证token过期刷新页面
             if(resp.status==401){
                 location.reload();
            parent.location.reload();
             }
             alert(resp.errmsg);
        });

    });
}


//用户信息保存
function save_User_Info() {
    $(".save_btn").click(function (e) {
        e.preventDefault();

        var signature = $("#signature").val();
        var nick_name = $("#nick_name").val();
        //过滤单选框被选择的value
        var gender = $("input[name='gender']").filter(":checked").val();

        if (!nick_name) {
            alert("请输入昵称");
            return;
        }
        if (!gender) {
            alert("请选择性别");
            return;
        }

        // TODO 修改用户信息接口
        params = {
            "signature":signature,
            "nick_name":nick_name,
            "gender":gender
        };
        $.ajax({
         url:host+"/user/"+user_id+"/info/",
         type:"put",
            data:JSON.stringify(params),
         headers:{
            "Authorization": "JWT " + token
        },
         contentType:"application/json"
    }).done(function (resp) {
        user_info = resp.data;
        $("#profile_url").attr("src",user_info.avatar_url);
        $("#signature").attr("placeholder",user_info.signature);
        $("#nick_name").attr("placeholder",user_info.username);

         if(user_info.gender == 1){
             $("input[name='gender']:eq(0)").prop("checked",true);
             $("input[name='gender']:eq(1)").prop("checked",false);
         }else {
             $("input[name='gender']:eq(1)").prop("checked",true);
             $("input[name='gender']:eq(0)").prop("checked",false);
         }
         sessionStorage.username =user_info.username;
         localStorage.username = user_info.username;
         alert("保存成功");
         parent.location.reload();
        }).fail(function (resp) {
            //如果签证token过期刷新页面
             if(resp.status==401){
                 location.reload();
            parent.location.reload();
             }
             alert(resp.errmsg);
        });




});
}


//修改用户密码
function changeUserPassword() {
    $(".password_save_btn").click(function (e) {
        e.preventDefault();

        var local_password = $("input[name='local_password']").val();
        var change_password = $("input[name='new_password']").val();
        var confirm_password = $("input[name='confirm_password']").val();

        if(!local_password || !change_password || !confirm_password){
            alert("输入框有空");
            return;
        }
        if(change_password!=confirm_password){
            alert("两次密码输入不一致");
            return;
        }
        params ={
            "local_password":local_password,
            "change_password":change_password,
            "confirm_password":confirm_password
        };

        $.ajax({
         url:host+"/user/"+user_id+"/password/",
         type:"put",
            data:JSON.stringify(params),
         headers:{
            "Authorization": "JWT " + token
        },
         contentType:"application/json"
    }).done(function (resp){
        alert("修改密码成功");
        sessionStorage.clear();
        localStorage.clear();
        parent.location.reload();
        })
            .fail(function (resp) {
            //如果签证token过期刷新页面
             if(resp.status==401){
                 location.reload();
            parent.location.reload();
             }
        }).fail(function (resp) {
            //如果签证token过期刷新页面
             if(resp.status==401){
                 location.reload();
            parent.location.reload();
             }
             alert(resp.errmsg);
        });



    });

}


$(function () {

    //添加图片,预览
    $("#user_img").change(function(e) {
        var imgBox = e.target;
        uploadImg($("#profile_url"), imgBox);
        $(".baseinfo >.form_group").prepend("<div style='margin-left: 150px;'>预览</div>");
    });



    //获取用户信息
    getUserInfo();

    //保存用户信息
    save_User_Info();

    //修改密码
    changeUserPassword();

    //上传用户头像
    UserImg();

});