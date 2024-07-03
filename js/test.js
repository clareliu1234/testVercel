// 导航栏点击触发active
$(document).ready(function () {
    // 遍历li标签，从而获取下面a标签的href，这里为了方便说明选用的是.nav类，在实际应用中可以使用id代替
    $('.col-12 col-lg-auto me-lg-auto mb-2 justify-content-center mb-md-0').find('li').each(function () {
        var a = $(this).find('a:first')[0];
        // 判断a标签的href是否与当前页面的路径相同
        if ($(a).attr("href") === location.pathname) {
            $(this).addClass("active");
        } else {
            $(this).removeClass("active");
        }
    })
    // 处理dropdown的情况，这里为了方便说明选用的是.dropdown-menu类，在实际应用中可以使用id代替
    $('.dropdown_menu').find('li').each(function () {
        var classname = $(this).attr('class');
        if (classname === 'active') {
            $('.dropdown-menu').addClass('active');
        }
    })
})