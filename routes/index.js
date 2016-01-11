var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function (req, res, next) {
    res.render('index', {title: 'Sketch Retrieval'});
});

router.get('/algorithms', function (req, res, next) {
    res.render('algo', {title: 'Sketch Based Image Retrieval'});
});

router.get('/about', function (req, res, next) {
    res.render('about', {title: 'Sketch Retrieval'});
});

module.exports = router;
