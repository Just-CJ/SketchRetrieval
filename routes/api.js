var express = require('express'),
    router = express.Router(),
    fs = require('fs'),
    path = require('path'),
    async = require('async'),
    spawn = require('child_process').spawn;

/* API list */
router.post('/submit', function (req, res, next) {
    var data = req.body,
        getIP = req.headers['x-forwarded-for'] || req.connection.remoteAddress,
        ip = getIP.split(':').pop(),
        time = new Date().getTime(),
        current = process.cwd(),
        fileName = 'tmp-' + ip + '-' + time + '.png',
        filePath = path.join(current, fileName);
    //var buffer = new Buffer(data.image, 'base64').toString('binary');
    async.waterfall([
        function (callback) {
            fs.writeFile(filePath, data.image, 'base64', function (err) {
                if (err) {
                    callback(err);
                    return;
                }
                var png = path.join(current, fileName);
                    python = path.join(current, 'python/online_process.py');
                callback(null, png, python);
            });
        },
        function (png, python, callback) {
            console.log(png);
            var result = [],
                err = [],
                child = spawn('python', [python, '-t', png, '-f', 'HOG']);
            child.stdout.on('data', function (data) {
                data = data.toString();
                result.push(data);
            });
            child.stderr.on('data', function (data) {
                data = data.toString();
                console.log(data);
                err.push(data);
            });
            child.on('exit', function () {
                var output = result.join('').split('\n');
                for(var i = 0; i < output.length; i++){
                    var item = {},
                        tmp = ('/' + output[i].replace(/\\/g, '/')).split(':');
                    item.image = tmp[0];
                    item.val = tmp[1];
                    output[i] = item;
                }
                output.length--;
                if(err.length != 0){
                    callback(err);
                    return;
                }
                callback(null, output);
            });
        }
    ], function (err, result) {
        if (err) {
            console.log(err);
            res.send(err);
            return;
        }
        _clearFile(filePath);
        res.json({
            "fileName": fileName,
            "images": result
        });
        //res.render('index', {
        //    title: 'Sketch Retrieval',
        //    img: '/tmp.png',
        //    images: result
        //});
    });
});

router.post('/upload', function () {

});

function _clearFile(path){
    fs.unlink(path, function(err){
        if(err){
            console.log(err);
            return;
        }
        console.log('Delete TmpFile: ' + path);
    })
}

module.exports = router;