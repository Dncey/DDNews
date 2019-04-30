
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

         });
}

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
         alert("保存成功");
         location.reload();
        });




})
}


//修改用户密码
function changeUserPassword() {
    $(".password_save_btn").click(function () {

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
        });



    });

}


$(function () {

    //获取用户信息
    getUserInfo();
    //保存用户信息
    save_User_Info();
    //修改密码
    changeUserPassword();

});