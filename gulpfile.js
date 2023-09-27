//===
// IMPORTS
//===
const { src, dest, parallel, series, watch } = require('gulp');
const browserSync = require('browser-sync').create();
const clean = require('gulp-clean');
const sass = require('gulp-dart-sass');
const sourcemaps = require('gulp-sourcemaps');
const ts = require('gulp-typescript');
const iconfont = require('gulp-iconfont');

//===
// VARIABLES
//===
const runTimestamp = Math.round(Date.now() / 1000);
const SRC_PATH = 'assets';
const DEST_PATH = 'static';

//===
// TASKS
//===
function cleanDist() {
    return src('static/*')
        .pipe(clean());
}

// Static server with reload
function initBrowserSync(cb) {
    browserSync.init({
        notify: false,
        open: false,
        proxy: 'http://django.localhost',
	ws: true,
	socket: {
	    domain: 'gulp-socket.localhost'
	}
    });
    return cb;
}

// Compile SASS + sourcemaps
function sassCompile() {
    return src([SRC_PATH + "/sass/desktop.sass", SRC_PATH + "/sass/mobile.sass"])
        .pipe(sourcemaps.init())
        .pipe(sass({outputStyle: 'compressed'}).on('error', sass.logError))
        .pipe(sourcemaps.write('.'))
        .pipe(dest(DEST_PATH + '/css/'))
        .pipe(browserSync.stream()) ;
}

// Compile Typescript to JavaScript
function typescript() {
    return src(SRC_PATH +'/ts/*.ts')
        .pipe(ts({
            noImplicitAny: true,
            outFile: 'main.js'
        }))
        .pipe(dest('static/js'))
        .pipe(browserSync.stream()) ;
}

// Copy images
function images() {
    return src(SRC_PATH +'/img/**/*')
        .pipe(dest(DEST_PATH + '/img/'))
        .pipe(browserSync.stream()) ;
}

// Build Font icons. *.svg to font-icons.woff2
function buildFontIcons() {
    return src(SRC_PATH + '/fonts/icons/*.svg')
        .pipe(iconfont({
            fontName: 'font-icons',
            prependUnicode: true,
            formats: ['woff2'],
            timestamp: runTimestamp
        }))
        .pipe(dest(DEST_PATH + '/fonts/'))
        .pipe(browserSync.stream()) ;
}

//===
// Tasks
//===

// Default: 'gulp'
const build = series(
    cleanDist,
    parallel(sassCompile, typescript, images, buildFontIcons)
);
exports.default = build;

// Dev: 'gulp dev'
exports.dev = function () {
    build();
    watch([SRC_PATH + '/sass/*.sass', SRC_PATH + '/sass/**/*.sass'], sassCompile);
    watch([SRC_PATH + '/ts/*.ts', SRC_PATH + '/ts/**/*.ts'], typescript);
    watch([SRC_PATH + '/img/*', SRC_PATH + '/img/**/*'], images);
    watch([SRC_PATH + '/fonts/icons/*.svg'], buildFontIcons);
    initBrowserSync();
}
