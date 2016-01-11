$(function(){
    $(document).on('updateImages', function (data) {
        window.g_images = data.images;
        window.g_fileName = data.fileName;
        updateImages();
    }).on('click', '.img', function(){
        var val = $(this).find('img').data('val');
        $('.value').html(val);
    });

    updateImages();

    function updateImages(){
        if(!window.g_images || window.g_images.length === 0){
            return;
        }
        var html = '',
            $imgWp = $('.img-wp');
        $imgWp.empty();
        for(var i = 0; i < window.g_images.length; i++){
            var tmp = window.g_images[i];
            html += '<div class="img fl"><img src="' + tmp.image + '" data-val="' + tmp.val + '" alt=""/></div>';
        }
        $imgWp.append(html);
    }
});