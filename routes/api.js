var express = require('express'),
    router = express.Router(),
    fs = require('fs'),
    path = require('path'),
    current = process.cwd(),
    async = require('async'),
    multer = require('multer'),
    uploader = multer({dest: path.join(current, 'uploads')}),
    spawn = require('child_process').spawn,
    python = path.join(current, 'python/online_process.py');

/* API list */
router.post('/submit', function (req, res, next) {
    var data = req.body,
        getIP = req.headers['x-forwarded-for'] || req.connection.remoteAddress,
        ip = getIP.split(':').pop(),
        time = new Date().getTime(),
        fileName = 'tmp-' + ip + '-' + time + '.png',
        filePath = path.join(current, fileName);
    async.waterfall([
        _savePaint(data, filePath),
        _retrieval
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
    });
});

router.post('/upload', uploader.single('file'), function (req, res, next) {
    var tmpPath = req.file.path,
        getIP = req.headers['x-forwarded-for'] || req.connection.remoteAddress,
        ip = getIP.split(':').pop(),
        time = new Date().getTime(),
        fileName = 'tmp-' + ip + '-' + time + '.png',
        targetPath = path.resolve('./uploads/' + fileName);
    async.waterfall([
        _saveUpload(tmpPath, targetPath),
        _retrieval
    ], function (err, result) {
        if (err) {
            console.log(err);
            res.send(err);
            return;
        }
        _clearFile(targetPath);
        res.json({
            "fileName": fileName,
            "images": result
        });
    });
});

function _savePaint(data, filePath) {
    return function (callback) {
        fs.writeFile(filePath, data.image, 'base64', function (err) {
            if (err) {
                callback(err);
                return;
            }
            callback(null, filePath);
        });
    }
}

function _saveUpload(tmpPath, targetPath) {
    return function (callback) {
        fs.rename(tmpPath, targetPath, function (err) {
            if (err) {
                callback(err);
                return;
            }
            callback(null, targetPath);
        });
    }
}

function _retrieval(png, callback) {
    var result = [],
        err = [],
        child = spawn('python', [python, '-t', png, '-f', 'HOG']);
    child.stdout.on('data', function (data) {
        data = data.toString();
        result.push(data);
    });
    child.stderr.on('data', function (data) {
        data = data.toString();
        //console.log(data);
        err.push(data);
    });
    child.on('exit', function () {
        var output = result.join('').split('\n');
        for (var i = 0; i < output.length; i++) {
            var item = {},
                tmp = ('/' + output[i].replace(/\\/g, '/')).split(':');
            item.image = tmp[0];
            item.val = tmp[1];
            output[i] = item;
        }
        output.length--;
        if (err.length != 0) {
            callback(err);
            return;
        }
        callback(null, output);
    });
}

function _clearFile(path) {
    fs.unlink(path, function (err) {
        if (err) {
            console.log(err);
            return;
        }
        console.log('Delete TmpFile: ' + path);
    });
}

module.exports = router;