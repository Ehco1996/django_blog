(function ( global, factory ) {
    'use strict';

    if ( typeof define === 'function' && define.amd ) {
        // AMD (Register as an anonymous module)
        define( 'autocjs', [ 'jquery' ], factory( global, $ ) );
    }
    else {
        if ( typeof define === 'function' && define.cmd ) {
            // CMD (Register as an anonymous module)
            define( 'autocjs', function ( require, exports, module ) {
                module.exports = factory( global, require( 'jquery' ) );
            } );
        }
        else {
            if ( typeof exports === 'object' ) {
                // Node/CommonJS
                module.exports = factory( global, require( 'jquery' ) );
            }
            else {
                // Browser globals
                factory( global, jQuery );
            }
        }
    }
}( typeof window !== 'undefined' ? window : this, function ( window, $ ) {
    'use strict';

    var HTML_CHARS = {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#x27;',
            '/': '&#x2F;',
            '`': '&#x60;'
        },
        SCRIPT_FRAGMENT = '<script[^>]*>([\\S\\s]*?)<\/script\\s*>',
        uid = -1,
        ARTICLE_PREFIX = 'article-',
        CLS_HEADING = 'autocjs-heading',
        CLS_ANCHOR = 'autocjs-anchor',
        CLS_WRAP = 'autocjs',
        CLS_CHAPTERS = 'autocjs-chapters',
        CLS_ARTICLE_CHAPTERS = ARTICLE_PREFIX + CLS_CHAPTERS,
        CLS_SUBJECTS = 'autocjs-subjects',
        CLS_CHAPTER = 'autocjs-chapter',
        CLS_TEXT = 'autocjs-text',
        CLS_CODE = 'autocjs-code',
        CLS_SHOW = 'autocjs-show',
        CLS_HIDE = 'autocjs-hide',
        ANCHOR = '<a class="' + CLS_ANCHOR + '" aria-hidden="true"></a>',
        WRAP = '<div id="{id}" class="' + CLS_WRAP + ' ' + CLS_HIDE + '" aria-hidden="true"></div>',
        HEADER = '<h2 class="autocjs-hd" aria-hidden="true">{title}</h2>',
        BODY = '<nav class="autocjs-bd" aria-hidden="true"></nav>',
        CHAPTERS = '<ol class="' + CLS_CHAPTERS + '" aria-hidden="true"></ol>',
        SUBJECTS = '<ol class="' + CLS_SUBJECTS + '" aria-hidden="true"></ol>',
        CHAPTER = '<li class="' + CLS_CHAPTER + '" aria-hidden="true"></li>',
        TEXT = '<a class="' + CLS_TEXT + '" aria-hidden="true"></a>',
        CODE = '<em class="' + CLS_CODE + '" aria-hidden="true"></em>',
        FOOTER = '<div class="autocjs-ft" aria-hidden="true"></div>',
        SWITCHER = '<h2 class="autocjs-switcher" title="Toggle Menu" aria-hidden="true">&#926;</h2>',
        TOP = '<a class="autocjs-top" href="#top" aria-hidden="true">TOP</a>',
        OVERLAY = '<div class="autocjs-overlay ' + CLS_HIDE + '" aria-hidden="true"></div>',
        SELECTOR = 'h1,h2,h3,h4,h5,h6';

    /**
     * 返回移除 JavaScript 代码后的字符串
     *
     * @method stripScripts
     * @param {String} html
     * @returns {String}
     */
    function stripScripts( html ) {
        return html.replace( new RegExp( SCRIPT_FRAGMENT, 'img' ), '' );
    }

    /**
     * 返回将 HTML 标签代码转义成对应的实体字符串
     *
     * @method encodeHTML
     * @param {String} html
     * @returns {String}
     */
    function encodeHTML( html ) {
        return html.replace( /[\r\t\n]/g, ' ' ).replace( /[&<>"'\/`]/g, function ( match ) {
            return HTML_CHARS[ match ];
        } );
    }

    /**
     * 返回将 HTML 实体字符串转义成对应的 HTML 标签代码
     *
     * @method decodeHTML
     * @param {String} html
     * @returns {String}
     */
    function decodeHTML( html ) {
        return html.replace( /&lt;/g, '<' )
                   .replace( /&gt;/g, '>' )
                   .replace( /&amp;/g, '&' )
                   .replace( /&quot;/g, '"' )
                   .replace( /&#x27;/g, '\'' )
                   .replace( /&#x2F;/g, '\/' )
                   .replace( /&#x60;/g, '`' );
    }

    /**
     * 返回安全的 HTML 代码：
     * 1. 移除 JS 代码；
     * 2. 转义 HTML 标签字符串
     * 3. 转义 HTML 实体字符串
     *
     * @method safetyHTML
     * @param {String} html
     * @returns {String}
     */
    function safetyHTML( html ) {
        return decodeHTML( encodeHTML( stripScripts( html ) ) );
    }

    /**
     * 一个简单的 HTML 模板工具，返回用 JSON 数据中的值替换特殊字符后 HTML 模板字符串。
     *
     * @method template
     * @param {Object} options - 配置参数
     * @param {Object} options.data - 模板的 JSON 对象格式数据
     * @param {String} options.html - 模板的 HTML 代码片段
     * @param {String} [options.startTag] - HTML 代码片段中特殊字符的开始标签
     * @param {String} [options.endTag] - HTML 代码片段中特殊字符的结束标签
     * @returns {String}
     */
    function template( options ) {
        var json = options.data,
            html = options.html,
            startTag = options.startTag || '{',
            endTag = options.endTag || '}';

        html += '';

        $.each( json, function ( key, value ) {
            html = html.replace( new RegExp( startTag + key + endTag, 'img' ), safetyHTML( value ) );
        } );

        return safetyHTML( html );
    }

    /**
     * 返回唯一的 id
     *
     * @method guid
     * @param {String} [prefix] - 可选，默认生成数字ID，设置了 prefix 则生成字符串ID
     * @returns {Number|String}
     */
    function guid( prefix ) {
        uid += 1;

        return prefix ? prefix + '-' + uid : uid;
    }

    /**
     * 根据两个相邻的标题标签的数字的差值，获得父级的 id 值
     *
     * @method getPidByDiffer
     * @param {Array} chapters -
     * @param {Number} differ -
     * @param {Number} index -
     * @returns {Number}
     */
    function getPidByDiffer( chapters, differ, index ) {
        var pid;

        // 最大只有5系的差距
        switch ( differ ) {
            case 1:
                pid = chapters[ chapters[ index - 1 ].pid ].pid;
                break;
            case 2:
                pid = chapters[ chapters[ chapters[ index - 1 ].pid ].pid ].pid;
                break;
            case 3:
                pid = chapters[ chapters[ chapters[ chapters[ index - 1 ].pid ].pid ].pid ].pid;
                break;
            case 4:
                pid = chapters[ chapters[ chapters[ chapters[ chapters[ index - 1 ].pid ].pid ].pid ].pid ].pid;
                break;
            case 5:
                pid = chapters[ chapters[ chapters[ chapters[ chapters[ chapters[ index - 1 ].pid ].pid ].pid ].pid ].pid ].pid;
                break;
            default:
                pid = chapters[ chapters[ index - 1 ].pid ].pid;
                break;
        }

        return pid;
    }

    /**
     * 返回 headings 对应的文章段落信息数据
     *
     * @returns {Array}
     */
    function getChapters( headings ) {
        var chapters = [],
            previous = 1,
            level = 0;


        // 获得目录索引信息
        $( headings ).each( function ( i, heading ) {
            var $heading = $( heading ),
                text = $heading.text(),
                rel = $heading.attr( 'rel' ) ? $heading.attr( 'rel' ) : '',
                current = parseInt( $heading[ 0 ].tagName.toUpperCase().replace( /[H]/ig, '' ), 10 ),
                pid = -1;

            // 1.（父标题，子标题）：当前标题的序号 > 前一个标题的序号
            if ( current > previous ) {
                level += 1;

                // 第一层级的 pid 是 -1
                if ( level === 1 ) {
                    pid = -1;
                }
                else {
                    pid = i - 1;
                }
            }
            else if ( current === previous || (current < previous && current > level) ) {

                // H1 的层级肯定是 1
                if ( current === 1 ) {
                    level = 1;

                    pid = -1;
                }
                else {
                    pid = chapters[ i - 1 ].pid;
                }
            }
            else if ( current <= level ) {

                // H1 的层级肯定是 1
                if ( current === 1 ) {
                    level = 1;
                }
                else {
                    level = level - (previous - current);
                }

                // 第一级的标题
                if ( level === 1 ) {
                    pid = -1;
                }
                else {
                    // 虽然看上去差点，不过能工作啊
                    pid = getPidByDiffer( chapters, previous - current, i );
                }
            }

            previous = current;

            chapters.push( {
                id: i,
                level: level,
                text: text,
                tag: heading.tagName,
                pid: pid,
                rel: rel
            } );
        } );

        return chapters;
    }

    /**
     * 返回 chapters 对应动态创建的标题锚点链接节点
     *
     * @param {Array} chapters
     * @param {String} anchorHTML
     * @returns {Array}
     */
    function getAnchors( chapters, anchorHTML ) {
        var anchors = [];

        $( chapters ).each( function ( i, chapter ) {
            var id = chapter.id,
                $anchor = $( anchorHTML ).attr( {
                    id: CLS_ANCHOR + '-' + id,
                    'href': '#' + CLS_HEADING + '-' + id,
                    'aria-label': chapter.text
                } ).addClass( CLS_ANCHOR ).addClass( CLS_HIDE );

            anchors.push( $anchor );
        } );

        return anchors;
    }

    /**
     * 返回 chapters 根据 pid 分组的文章段落数据
     *
     * @param chapters
     * @returns {Array}
     */
    function getList( chapters ) {
        var temp = {},
            list = [];

        $( chapters ).each( function ( i, chapter ) {
            var key = chapter.pid === -1 ? 'H1' : chapter.pid.toString();

            if ( !temp[ key ] ) {
                temp[ key ] = [];
            }
        } );

        $.each( temp, function ( key ) {
            $( chapters ).each( function ( i, chapter ) {
                var pid = chapter.pid === -1 ? 'H1' : chapter.pid.toString();

                if ( key === pid ) {
                    temp[ key ].push( chapter );
                }
            } );

            list.push( temp[ key ] );
        } );

        return list;
    }

    /**
     * AutocJS 构造函数
     *
     * @constructor
     * @class AutocJS
     * @param {Object} options - 初始化的配置信息
     * @param {String|HTMLElement} options.article - 页面中显示文章正文的 DOM 节点或者 ID 选择器
     * @param {String} [options.selector] - 标题标签的选择器，例如：'h1,h2,h3,h4,h5,h6'
     * @param {String} [options.headingPrefix] - 标题标签节点自动添的 id 属性的前缀，默认值：'autocjs-heading'
     * @param {String} [options.title] - 导航菜单的标题文字，默认值：'Table of Contents'
     * @param {Boolean} [options.isOnlyAnchors] - 是否只创建标题链接，默认值：false
     * @param {Boolean} [options.isAnimateScroll] - 是否使用动画滚动定位，默认值：true
     * @param {Boolean} [options.hasDirectoryInArticle] - 是否在文章中创建目录导航，默认值：false
     * @param {Boolean} [options.hasChapterCodeAtHeadings] - 是否在文章标题中显示该标题的段落索引编号，默认值：false
     * @param {String} [options.ANCHOR] - 标题标签中创建的标题链接的 HTML 模板代码
     * @param {String} [options.WRAP] - AutocJS 菜单根节点的 HTML 模板代码
     * @param {String} [options.HEADER] - AutocJS 菜单标题栏的 HTML 模板代码
     * @param {String} [options.BODY] - AutocJS 菜单内容节点的 HTML 模板代码
     * @param {String} [options.FOOTER] - AutocJS 菜单页脚节点的 HTML 模板代码
     * @param {String} [options.SWITCHER] - AutocJS 菜单展开显示开关的 HTML 模板代码
     * @param {String} [options.TOP] - AutocJS 菜单返回顶部按钮的 HTML 模板代码
     * @param {String} [options.CHAPTERS] - AutocJS 导航目录列表的 HTML 模板代码
     * @param {String} [options.SUBJECTS] - AutocJS 导航子目录列表的 HTML 模板代码
     * @param {String} [options.CHAPTER] - AutocJS 导航段落章节的 HTML 模板代码
     * @param {String} [options.TEXT] - AutocJS 导航段落章节链接的 HTML 模板代码
     * @param {String} [options.CODE] - AutocJS 段落章节索引编码的 HTML 模板代码
     * @param {String} [options.OVERLAY] - AutocJS 菜单展开时遮罩层的 HTML 模板代码
     * @returns {AutocJS}
     */
    var AutocJS = function ( options ) {

        /**
         * 存储的是 AutocJS 对象当前的所有配置信息
         *
         * @property
         * @see AutocJS.defaults
         * @private
         */
        this.attributes = {};

        /**
         * 存储的是 AutocJS 对象相关的所有 DOM 元素
         *
         * @property
         * @private
         */
        this.elements = {
            // 文章正文内容容器 DOM 元素
            article: null,
            // 文章中的所有（selector 匹配）的标题 DOM 元素
            headings: null,
            // 将 hasDirectoryInArticle 参数设置为 true 时，在文章正文开始处创建的目录导航列表 DOM 节点
            chapters: null,
            // AutocJS 对象创建的目录导航菜单的根节点
            wrap: null,
            // AutocJS 对象创建的目录导航菜单的标题栏 DOM 节点
            header: null,
            // AutocJS 对象创建的目录导航菜单的正文内容 DOM 节点
            body: null,
            // AutocJS 对象创建的目录导航菜单的列表 DOM 节点
            list: null,
            // AutocJS 对象创建的目录导航菜单的页脚 DOM 节点
            footer: null,
            // AutocJS 对象创建的目录导航菜单的隐藏显示开关 DOM 节点
            switcher: null,
            // AutocJS 对象创建的目录导航菜单中的返回顶部 DOM 节点
            top: null,
            // AutocJS 对象创建的目录导航菜单的遮罩层 DOM 节点
            overlay: null
        };

        /**
         * 存储的是 AutocJS 根据标题 DOM 元素分析的数据：
         * 1. chapters 标题章节索引数据；
         * 2. anchors 各个标题对应的标题锚点链接 DOM 元素
         * 3. list 将 chapters 数据按 pid 属性分组后的章节索引数据
         *
         * <pre>
         * <code>
         * // 单个 chapter 数据示例
         * {
         *    // id 编号
         *    id: 0,
         *    // 标题节点标签的层级级别
         *    level: 1,
         *    // 标题节点的文字
         *    text: '文章标题',
         *    // 标题节点 tagName.toUpperCase()
         *    tag: 'H1',
         *    // 标题节点的父级节点　id 编号
         *    pid: 0,
         *    // 标题外部链接
         *    rel: 'http://www.yaohaixiao.com/'
         * }
         * </code>
         * </pre>
         * @property
         * @private
         */
        this.data = {
            chapters: [],
            anchors: [],
            list: []
        };

        this.set( AutocJS.defaults ).init( options );

        return this;
    };

    /**
     * AutocJS 对象默认配置选项
     *
     * @property
     * @static
     */
    AutocJS.defaults = {
        // 页面中显示文章正文的 DOM 节点或者 ID 选择器
        article: '',
        // 标题标签的选择器，默认值：'h1,h2,h3,h4,h5,h6'
        selector: SELECTOR,
        // AutocJS 自动创建的导航菜单标题文字，默认值：'Table of Contents'
        title: 'Table of Contents',
        // 是否只创建标题链接，默认值：false
        isAnchorsOnly: false,
        // 是否使用动画滚动定位，默认值：true
        isAnimateScroll: true,
        // 是否在文章中创建目录导航，默认值：false
        hasDirectoryInArticle: false,
        // 是否在文章标题中显示该标题的段落索引编号，默认值：false
        hasChapterCodeAtHeadings: false,
        // 是否在导航菜单中显示段落索引编号，默认值：true
        hasChapterCodeInDirectory: true,
        // 标题标签中创建的标题链接的 HTML 模板代码
        ANCHOR: ANCHOR,
        // AutocJS 菜单根节点的 HTML 模板代码
        WRAP: WRAP,
        // AutocJS 菜单标题栏的 HTML 模板代码
        HEADER: HEADER,
        // AutocJS 菜单内容节点的 HTML 模板代码
        BODY: BODY,
        // AutocJS 菜单页脚节点的 HTML 模板代码
        FOOTER: FOOTER,
        // AutocJS 菜单展开显示开关的 HTML 模板代码
        SWITCHER: SWITCHER,
        // AutocJS 菜单返回顶部按钮的 HTML 模板代码
        TOP: TOP,
        // AutocJS 导航目录列表的 HTML 模板代码
        CHAPTERS: CHAPTERS,
        // AutocJS 导航子目录列表的 HTML 模板代码
        SUBJECTS: SUBJECTS,
        // AutocJS 导航段落章节的 HTML 模板代码
        CHAPTER: CHAPTER,
        // AutocJS 导航段落章节链接的 HTML 模板代码
        TEXT: TEXT,
        // AutocJS 段落章节索引编码的 HTML 模板代码
        CODE: CODE,
        // AutocJS 菜单展开时遮罩层的 HTML 模板代码
        OVERLAY: OVERLAY
    };

    AutocJS.stripScripts = stripScripts;
    AutocJS.encodeHTML = encodeHTML;
    AutocJS.decodeHTML = decodeHTML;
    AutocJS.safetyHTML = safetyHTML;
    AutocJS.template = template;
    AutocJS.guid = guid;

    AutocJS.prototype = {
        version: '1.2.0',
        constructor: AutocJS,
        /**
         * 初始化方法：
         * 1. set() 初始化配置参数
         * 2. initElements() 初始化所有 DOM 元素
         * 3. initData() 初始化数据
         * 4. render() 绘制 UI 界面
         * 5. attachEvents 给 AutocJS 相关的 DOM 元素绑定事件处理器
         *
         * @param {Object} options - 配置信息
         * @see AutocJS.defaults
         * @returns {AutocJS}
         */
        init: function ( options ) {

            if ( $.isPlainObject( options ) ) {
                this.set( options );
            }

            this.initElements()
                .initData()
                .render()
                .attachEvents();

            return this;
        },
        /**
         * 初始化 elements 属性（AutocJS 对象相关 DOM 元素）
         *
         * @since 1.0.0
         * @returns {AutocJS}
         */
        initElements: function () {
            var self = this,
                elements = this.dom();

            // 初始化文章中存在的 DOM 元素
            elements.article = $( this.get( 'article' ) );
            elements.headings = elements.article.find( this.get( 'selector' ) );

            // 初始化动态创建的 DOM 元素
            elements.chapters = $( this.get( 'CHAPTERS' ) ).addClass( CLS_ARTICLE_CHAPTERS );
            elements.wrap = $( template( {
                data: {
                    id: guid( CLS_WRAP )
                },
                html: self.get( 'WRAP' )
            } ) );
            elements.header = $( template( {
                data: {
                    title: self.get( 'title' )
                },
                html: self.get( 'HEADER' )
            } ) );
            elements.body = $( this.get( 'BODY' ) );
            elements.list = $( this.get( 'CHAPTERS' ) );
            elements.footer = $( this.get( 'FOOTER' ) );
            elements.switcher = $( this.get( 'SWITCHER' ) );
            elements.top = $( this.get( 'TOP' ) );
            elements.overlay = $( this.get( 'OVERLAY' ) );

            return this;
        },
        /**
         * 初始化 data 属性（文章段落章节数据）
         *
         * @since 1.0.0
         * @returns {AutocJS}
         */
        initData: function () {
            var data = this.data;

            data.chapters = getChapters( this.headings() );

            data.anchors = getAnchors( this.chapters(), this.get( 'ANCHOR' ) );

            data.list = getList( this.chapters() );

            return this;
        },
        /**
         * （根据新的配置信息）重启程序：
         * 1. destroy() 先移除所有绘制的 DOM 元素和绑定的事件处理器
         * 2. init() 重新初始化程序
         *
         * @param {Object} [options] - 配置信息
         * @see AutocJS.defaults
         * @returns {AutocJS}
         */
        reload: function ( options ) {

            this.destroy().init( options );

            return this;
        },
        /**
         * 设置 attributes 属性
         *
         * @param {Object} options
         * @see AutocJS.defaults
         * @returns {AutocJS}
         */
        set: function ( options ) {

            if ( $.isPlainObject( options ) ) {
                $.extend( this.attributes, options );
            }

            return this;
        },
        /**
         * 返回某个 attributes 属性
         *
         * @param {String} prop - attributes 属性名称
         * @returns {String|Boolean}
         */
        get: function ( prop ) {
            return this.attributes[ prop ];
        },
        /**
         * 返回 elements 属性，AutocJS 对象创建的所有 DOM 元素
         *
         * @since 1.0.0
         * @returns {Object}
         */
        dom: function () {
            return this.elements;
        },
        /**
         * 返回页面中的文章正文容器 DOM 元素
         *
         * @since 1.0.0
         * @returns {HTMLElement}
         */
        article: function () {
            // 获得文章内容的 DOM 节点
            return this.dom().article;
        },
        /**
         * 返回 article 中 selector 匹配的所有标题 DOM 元素
         *
         * @returns {AutocJS|Array}
         */
        headings: function () {
            return this.dom().headings;
        },
        /**
         * 传入 headings 参数，则设置 data.chapters 属性，如果设置 isSilent 为 true，则会更新所有的章节导航，返回 AutocJS 对象。
         * 没有传入 headings 数据，则返回 data.chapters 属性。
         *
         * @param {Array} [headings] - 标题标签 DOM 元素数组
         * @param {Boolean} [isSilent] - 是否安静更新数据，默认值：true
         * @returns {AutocJS|Array}
         */
        chapters: function ( headings, isSilent ) {
            isSilent = isSilent === false ? false : true;

            if ( headings ) {
                this.data.chapters = getChapters( headings );

                if ( !isSilent ) {

                    if ( this.get( 'hasDirectoryInArticle' ) ) {
                        this.renderArticleChapters();
                    }

                    if ( !this.get( 'isAnchorsOnly' ) ) {
                        this.renderSidebarChapters();
                    }
                }
            }
            else {
                return this.data.chapters;
            }

            return this;
        },
        /**
         * 返回 data.anchors 属性
         *
         * @returns {Array}
         */
        anchors: function () {
            return this.data.anchors;
        },
        /**
         * 返回 data.list 属性
         *
         * @since 1.0.0
         * @returns {Array}
         */
        list: function () {
            return this.data.list;
        },
        /**
         * 返回 chapter 在 list() 返回的数据中对应段落层次位置索引值
         *
         * @param {Object} chapter - 某个文章标题对应的段落章节信息
         * @returns {Number}
         */
        getChapterIndex: function ( chapter ) {
            var index = -1;

            $( this.list() ).each( function ( i, list ) {
                $( list ).each( function ( j, data ) {
                    if ( data === chapter ) {
                        index = j;
                        return false;
                    }
                } );
            } );

            return index;
        },
        /**
         * 绘制 UI 界面
         * 1. renderArticleDirectory() 绘制文章开始出的目录导航
         * 2. renderAnchors() 绘制标题栏的锚点链接和标题段落索引编码
         * 3. renderSidebarDirectory() 绘制侧边栏的目录导航菜单
         *
         * @returns {AutocJS}
         */
        render: function () {

            this.renderArticleDirectory()
                .renderAnchors()
                .renderSidebarDirectory();

            return this;
        },
        /**
         * 当设置了 hasDirectoryInArticle 为 true 时，则在文章开始处绘制目录导航
         *
         * @since 1.0.0
         * @returns {AutocJS}
         */
        renderArticleDirectory: function () {
            var $first = $( this.article()[ 0 ].firstChild );

            if ( !this.get( 'hasDirectoryInArticle' ) ) {
                return this;
            }

            this.dom().chapters.insertBefore( $first );

            this.renderArticleChapters();

            return this;
        },
        /**
         * 绘制文章中的目录导航的具体章节内容
         *
         * @since 1.0.0
         * @returns {AutocJS}
         */
        renderArticleChapters: function () {

            if ( this.get( 'hasDirectoryInArticle' ) ) {
                this.renderChapters( this.dom().chapters );
            }

            return this;
        },
        /**
         * 绘制标题锚点链接（这个是借鉴的 AnchorsJS 的思路）和标题段落章节索引代码
         *
         * @see AnchorJS: http://bryanbraun.github.io/anchorjs/
         * @returns {AutocJS}
         */
        renderAnchors: function () {
            var self = this,
                headings = this.headings(),
                anchors = this.anchors();

            $( this.chapters() ).each( function ( i, chapter ) {
                var id = CLS_HEADING + '-' + chapter.id,
                    $heading = $( headings[ i ] ),
                    $existingAnchor = $heading.find( '#' + id ),
                    $anchor = $( anchors[ i ] );

                if ( $existingAnchor[ 0 ] ) {
                    $existingAnchor.remove();
                }

                $heading.attr( 'id', id )
                        .addClass( CLS_HEADING )
                        .append( $anchor );

                self.renderHeadingChapterCode( chapter );
            } );

            return this;
        },
        /**
         * 在文章标题中绘制其对应的段落章节索引编码
         *
         * @since 1.0.0
         * @param {Object} chapter - 某个文章标题对应的段落章节信息
         * @returns {AutocJS}
         */
        renderHeadingChapterCode: function ( chapter ) {
            var CODE = ARTICLE_PREFIX + CLS_CODE,
                pid = chapter.pid,
                id = chapter.id,
                tag = chapter.tag,
                $anchor = $( '#' + CLS_HEADING + '-' + id ),
                $existingCode = $anchor.find( '#' + CODE + '-' + id ),
                $code,
                chapterCode,
                chapterIndex;

            if ( $existingCode[ 0 ] ) {
                $existingCode.remove();
            }

            if ( !this.get( 'hasChapterCodeAtHeadings' ) || tag === 'H1' ) {
                return this;
            }

            $code = $( this.get( 'CODE' ) ).attr( 'id', CODE + '-' + id );

            // 绘制章节索引
            chapterIndex = this.getChapterIndex( chapter ) + 1;

            if ( pid === -1 && tag === 'H2' ) {
                chapterCode = chapterIndex;
            }
            else {
                chapterCode = $( '#' + CODE + '-' + pid ).html() + '.' + chapterIndex;
            }

            // 绘制段落章节编码
            $code.attr( 'data-chapter', chapterCode ).html( chapterCode );
            $code.insertBefore( $anchor[ 0 ].firstChild );

            return this;
        },
        /**
         * 绘制侧边栏的目录导航菜单
         *
         * @since 1.0.0
         * @returns {AutocJS}
         */
        renderSidebarDirectory: function () {

            if ( this.get( 'isAnchorsOnly' ) ) {
                return this;
            }

            // 绘制导航菜单框架
            // 绘制导航链接
            this.renderSidebarOutline().renderSidebarChapters();

            // 全部绘制完成，再显示完整的菜单
            this.dom().wrap.removeClass( CLS_HIDE );

            // 最后更新菜单的高度
            this.updateLayout();

            return this;
        },
        /**
         * 绘制侧边栏菜单的框架
         *
         * @since 1.0.0
         * @returns {AutocJS}
         */
        renderSidebarOutline: function () {
            var elements = this.dom(),
                $wrap = elements.wrap,
                $footer = elements.footer,
                $body = $( document.body );

            if ( this.get( 'isAnchorsOnly' ) ) {
                return this;
            }

            // 绘制head
            $footer.append( elements.switcher ).append( elements.top );

            // 绘制body
            elements.body.append( elements.list );

            // 绘制完整的导航
            $wrap.empty().append( elements.header ).append( elements.body ).append( $footer );

            // 将导航和遮罩层添加到页面
            $body.append( $wrap ).append( elements.overlay );

            if ( !this.get( 'isAnimateScroll' ) ) {
                $body.attr( 'id', 'top' );
            }

            return this;
        },
        /**
         * 绘制侧边栏导航菜单中的目录导航的具体章节内容
         *
         * @since 1.0.0
         * @returns {AutocJS}
         */
        renderSidebarChapters: function () {

            if ( !this.get( 'isAnchorsOnly' ) ) {
                this.renderChapters( this.dom().list );
            }

            return this;
        },
        /**
         * 绘制文章章节索引
         *
         * @returns {AutocJS}
         */
        renderChapters: function ( list ) {
            var self = this,
                $list = $( list ),
                chapters = this.chapters();

            $list.empty();

            $( chapters ).each( function ( i, chapter ) {
                var pid = chapter.pid,
                    id = chapter.id,
                    headingId = CLS_HEADING + '-' + id,
                    url = chapter.rel ? chapter.rel : '#' + headingId,
                    $chapter = $( self.get( 'CHAPTER' ) ),
                    $code = $( self.get( 'CODE' ) ),
                    $text = $( self.get( 'TEXT' ) ),
                    $subjects,
                    $parent,
                    chapterCode,
                    chapterIndex,
                    linkId,
                    chapterId,
                    subjectId,
                    parentId;

                if ( $list.hasClass( CLS_ARTICLE_CHAPTERS ) ) {
                    linkId = ARTICLE_PREFIX + CLS_TEXT + '-' + id;
                    chapterId = ARTICLE_PREFIX + CLS_CHAPTER + '-' + id;
                    subjectId = ARTICLE_PREFIX + CLS_SUBJECTS + '-' + pid;
                    parentId = ARTICLE_PREFIX + CLS_CHAPTER + '-' + pid;
                }
                else {
                    linkId = CLS_TEXT + '-' + id;
                    chapterId = CLS_CHAPTER + '-' + id;
                    subjectId = CLS_SUBJECTS + '-' + pid;
                    parentId = CLS_CHAPTER + '-' + pid;
                }

                $subjects = $( '#' + subjectId );

                // 创建菜单的链接
                $text.attr( {
                    id: linkId,
                    href: url,
                    rel: headingId
                } ).html( chapter.text );

                // 创建菜单项
                $chapter.attr( {
                    'id': chapterId,
                    'title': chapter.text
                } ).append( $text );

                // 一级标题直接创建标题链接即可
                if ( chapter.pid === -1 ) {

                    $list.append( $chapter );
                    chapterIndex = $chapter.index() + 1;
                    chapterCode = chapterIndex;

                }
                else {

                    // 子级的标题，需要找到上级章节
                    $parent = $( '#' + parentId );

                    // 没有绘制子菜单，则绘制它
                    if ( !$subjects[ 0 ] ) {
                        $subjects = $( self.get( 'SUBJECTS' ) ).attr( 'id', subjectId );

                        $parent.append( $subjects );
                    }

                    $subjects.append( $chapter );

                    // 绘制章节索引
                    chapterIndex = $chapter.index() + 1;
                    chapterCode = $parent.find( '.' + CLS_CODE ).html() + '.' + chapterIndex;
                }

                if ( self.get( 'hasChapterCodeInDirectory' ) ) {
                    // 绘制段落章节编码
                    $code.attr( 'data-chapter', chapterCode ).html( chapterCode );
                    $code.insertBefore( $text );
                }
            } );

            return this;
        },
        /**
         * 展开侧边栏菜单
         *
         * @returns {AutocJS}
         */
        show: function () {
            var elements = this.dom(),
                $wrap = elements.wrap;

            elements.overlay.removeClass( CLS_HIDE );

            $wrap.animate( {
                left: 0
            }, 150, function () {
                $wrap.addClass( CLS_SHOW );
            } );

            return this;
        },
        /**
         * 收起侧边栏菜单
         *
         * @returns {AutocJS}
         */
        hide: function () {
            var elements = this.dom(),
                $wrap = elements.wrap;

            $wrap.animate( {
                left: -300
            }, 150, function () {
                elements.overlay.addClass( CLS_HIDE );
                $wrap.removeClass( CLS_SHOW );
            } );

            return this;
        },
        /**
         * 收起/展开侧边栏菜单
         *
         * @returns {AutocJS}
         */
        toggle: function () {

            if ( this.dom().wrap.hasClass( CLS_SHOW ) ) {
                this.hide();
            }
            else {
                this.show();
            }

            return this;
        },
        /**
         * 更新侧边栏菜单界面高度
         *
         * @returns {AutocJS}
         */
        updateLayout: function () {
            var elements = this.dom(),
                wrapHeight = elements.wrap[ 0 ].offsetHeight,
                headerHeight = elements.header[ 0 ].offsetHeight;

            elements.body.height( wrapHeight - headerHeight );

            return this;
        },
        /**
         * 将窗口的滚动条滚动到指定 top 值的位置
         *
         * @param {Number} top
         * @returns {AutocJS}
         */
        scrollTo: function ( top ) {
            var self = this;

            $( "html,body" )
                .animate( {
                    scrollTop: top
                }, 500, 'linear', function () {
                    self.hide();
                } );

            return this;
        },
        /**
         * 移除所有绘制的 DOM 节点，并移除绑定的事件处理器
         *
         * @returns {AutocJS}
         */
        destroy: function () {
            var $headings = this.headings(),
                elements = this.dom(),
                $article = this.article(),
                $chapters = elements.chapters,
                $wrap = elements.wrap,
                $overlay = elements.overlay;

            $article.off();

            $chapters.remove();

            $( $headings ).each( function ( i, heading ) {
                var $heading = $( heading ),
                    $anchors = $heading.find( '.' + CLS_ANCHOR ),
                    $code = $heading.find( '.' + CLS_CODE );

                $heading.removeClass( CLS_HEADING ).removeAttr( 'id' );
                $code.remove();

                $anchors.remove();
            } );

            $wrap.off().remove();

            $overlay.off().remove();

            $( window ).off( 'resize', this.onWindowResize );

            return this;
        },
        /**
         * 给 AutocJS 相关的所有 DOM 节点绑定事件处理器
         *
         * @returns {AutocJS}
         */
        attachEvents: function () {
            var self = this,
                elements = this.dom(),
                $article = this.article(),
                data = {
                    context: self
                };

            // 鼠标滑过标题，显示标题的 AutocJS 链接
            $article.delegate( '.' + CLS_HEADING, 'mouseenter', data, this.onHeadingMouseEnter );

            // 鼠标离开标题，隐藏标题的 AutocJS 链接
            $article.delegate( '.' + CLS_HEADING, 'mouseleave', data, this.onHeadingMouseLeave );

            if ( this.get( 'hasDirectoryInArticle' ) ) {
                $article.delegate( '.' + CLS_TEXT, 'click', data, this.onArticleChapterClick );
            }

            if ( !this.get( 'isAnchorsOnly' ) ) {

                // 点击目录标题，隐藏/显示目录导航
                elements.switcher.on( 'click', data, this.onSwitcherClick );

                // 点击TOP链接，返回页面顶部
                elements.top.on( 'click', data, this.onTopClick );

                // 点击导航，定位文章，收起导航
                elements.list.delegate( '.' + CLS_TEXT, 'click', data, this.onSidebarChapterClick );

                // 点击遮罩层，收起导航
                elements.overlay.on( 'click', data, this.onOverlayClick );

                $( window ).on( 'resize', data, this.onWindowResize );
            }

            return this;
        },
        /**
         * 文章标题节点 mouseenter 事件处理器。在鼠标滑过文章标题，显示自动创建的锚点链接。
         *
         * @param {Event} evt - Event 对象
         * @returns {AutocJS}
         */
        onHeadingMouseEnter: function ( evt ) {
            var context = evt.data.context,
                $anchor = $( this ).find( '.' + CLS_ANCHOR );

            $anchor.removeClass( CLS_HIDE );

            return context;
        },
        /**
         * 文章标题节点 mouseleave 事件处理器。在鼠标离开文章标题，隐藏自动创建的锚点链接。
         *
         * @param {Event} evt - Event 对象
         * @returns {AutocJS}
         */
        onHeadingMouseLeave: function ( evt ) {
            var context = evt.data.context,
                $anchor = $( this ).find( '.' + CLS_ANCHOR );

            $anchor.addClass( CLS_HIDE );

            return context;
        },
        /**
         * 文章开始处文章导航链接的 click 事件处理器。点击链接时，滚动定位到相应的段落开始位置。
         *
         * @param {Event} evt - Event 对象
         * @returns {AutocJS}
         */
        onArticleChapterClick: function ( evt ) {
            var context = evt.data.context,
                isAnimateScroll = context.get( 'isAnimateScroll' ),
                $chapter = $( '#' + $( this ).attr( 'rel' ) );

            if ( isAnimateScroll ) {
                context.scrollTo( $chapter[ 0 ].offsetTop );

                evt.stopPropagation();
                evt.preventDefault();
            }

            return context;
        },
        /**
         * 侧边栏菜单的展开/收起按钮的 click 事件处理器。点击后会根据菜单展开状态，展开或收起，并且隐藏遮罩层。
         *
         * @param {Event} evt - Event 对象
         * @returns {AutocJS}
         */
        onSwitcherClick: function ( evt ) {
            var context = evt.data.context;

            context.toggle();

            evt.stopPropagation();
            evt.preventDefault();

            return context;
        },
        /**
         * 侧边栏菜单的返回顶部按钮菜单的 click 事件处理器。点击后会滚动到页面顶部，并且隐藏遮罩层，收起菜单。
         *
         * @param {Event} evt - Event 对象
         * @returns {AutocJS}
         */
        onTopClick: function ( evt ) {
            var context = evt.data.context,
                isAnimateScroll = context.get( 'isAnimateScroll' );

            if ( isAnimateScroll ) {
                context.scrollTo( 0 );

                evt.stopPropagation();
                evt.preventDefault();
            }
            else {
                context.hide();
            }

            return context;
        },
        /**
         * 侧边栏菜单的文章索引链接的 click 事件处理器。点击后会会滚动定位到文章相关章节标题的位置，并且隐藏遮罩层，收起菜单。
         *
         * @param {Event} evt - Event 对象
         * @returns {AutocJS}
         */
        onSidebarChapterClick: function ( evt ) {
            var context = evt.data.context,
                isAnimateScroll = context.get( 'isAnimateScroll' ),
                $chapter = $( '#' + $( this ).attr( 'rel' ) );

            if ( isAnimateScroll ) {
                context.scrollTo( $chapter[ 0 ].offsetTop );

                evt.stopPropagation();
                evt.preventDefault();
            }
            else {
                context.hide();
            }

            return context;
        },
        /**
         * 遮罩层的 click 事件处理器。点击后隐藏遮罩层，收起菜单。
         *
         * @param {Event} evt - Event 对象
         * @returns {AutocJS}
         */
        onOverlayClick: function ( evt ) {
            var context = evt.data.context;

            context.hide();

            evt.stopPropagation();
            evt.preventDefault();

            return context;
        },
        /**
         * 窗口的 resize 事件处理器。窗口大小变更后，将立即更新侧边栏高度。
         *
         * @param {Event} evt - Event 对象
         * @returns {AutocJS}
         */
        onWindowResize: function ( evt ) {
            var context = evt.data.context;

            context.updateLayout();

            return context;
        }
    };

    // 将 autoc 扩展为一个 jquery 插件
    $.extend( $.fn, {
        autoc: function ( options ) {
            var $article = $( this ),
                config = {};

            $.extend( config, options, {
                article: $article
            } );

            return new AutocJS( config );
        }
    } );

    window.AutocJS = AutocJS;

    return AutocJS;
} ));