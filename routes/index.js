var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function (req, res, next) {
    res.render('index', {
        demo: true,
        title: 'Sketch Retrieval'
    });
});

router.get('/algo', function (req, res, next) {
    res.render('algo', {
        algo: true,
        title: 'Sketch Based Image Retrieval'
    });
});

router.get('/about', function (req, res, next) {
    res.render('about', {
        about: true,
        title: 'Sketch Retrieval'
    });
});

module.exports = router;
