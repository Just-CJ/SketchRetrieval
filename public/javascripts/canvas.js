$(function () {
    var canvas = $('.paint-board')[0],
        context = canvas.getContext('2d'),
        _width = 300,
        _height = 300,
        paint = false,
        x, y, lastPos = {};

    _initCanvas();
    _clearCanvas();

    $('.left-part').on('mousedown', '.paint-board', mouseDownEvent)
        .on('mousemove', '.paint-board', mouseMoveEvent)
        .on('mouseup mouseleave', '.paint-board', mouseUpEvent)
        .on('click', '.btn-clear', _clearCanvas)
        .on('click', '.btn-submit', submitCanvas)
        .on('click', '.btn-upload', uploadImg);


    function _initCanvas() {
        canvas.width = _width;
        canvas.height = _height;
        context.strokeStyle = 'black';
        context.lineJoin = 'round';
        context.lineWidth = 5;
    }

    function _clearCanvas() {
        context.clearRect(0, 0, _width, _height);
        context.fillStyle = '#FFFFFF';
        context.fillRect(0, 0, _width, _height);
    }

    function mouseDownEvent(e) {
        e.preventDefault();
        paint = true;
        x = e.clientX;
        y = e.clientY;
        draw(x - this.offsetLeft, y - this.offsetTop);
    }

    function mouseMoveEvent(e) {
        e.preventDefault();
        if (paint) {
            x = e.clientX;
            y = e.clientY;
            draw(x - this.offsetLeft, y - this.offsetTop);
        }
    }

    function mouseUpEvent(e) {
        e.preventDefault();
        if (paint) {
            paint = false;
            lastPos = null;
        }
    }

    function draw(posX, posY) {
        context.beginPath();
        if (lastPos) {
            context.moveTo(lastPos[0], lastPos[1]);
            context.lineTo(posX, posY);
        }
        context.closePath();
        context.stroke();
        lastPos = [posX, posY];
    }

    function submitCanvas(e) {
        e.preventDefault();
        var $this = $(this),
            $overlay = $('.overlay');

        if ($this.hasClass('disabled')) {
            return;
        }

        $this.addClass('disabled btn-disabled');
        $overlay.css({display: 'block'});

        var data = canvas.toDataURL('image/png'),
        //delete img info
            data = data.substring(22);
        $.ajax({
            type: 'POST',
            url: '/api/submit',
            //async: true,
            data: {
                image: data
            },
            success: function (ajaxData) {
                //var result = JSON.parse(images);
                //console.log(ajaxData.images);
                $(document).triggerHandler({
                    type: 'updateImages',
                    images: ajaxData.images,
                    fileName: ajaxData.fileName
                });
            },
            error: function (xhr, textStatus) {
                console.log(textStatus);
                //$('#error-info').text(textStatus).show();
            },
            complete: function () {
                $this.removeClass('disabled btn-disabled');
                $overlay.css({display: 'none'});
            }
        });
    }

    function uploadImg(e) {
        e.preventDefault();
        var $this = $(this);
        if ($this.hasClass('disabled')) {
            return;
        }
        $this.addClass('disabled btn-disabled');
        $('.J-upload').click();
        $this.removeClass('disabled btn-disabled');
    }
});