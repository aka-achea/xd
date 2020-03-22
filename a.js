(function() {
    function a(a) {
        var d, e, b = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", c = "";
        for (d = 0; a > d; d += 1)
            e = Math.random() * b.length,
            e = Math.floor(e),
            c += b.charAt(e);
        return c
    }
    function b(a, b) {
        var c = CryptoJS.enc.Utf8.parse(b)
          , d = CryptoJS.enc.Utf8.parse("0102030405060708")
          , e = CryptoJS.enc.Utf8.parse(a)
          , f = CryptoJS.AES.encrypt(e, c, {
            iv: d,
            mode: CryptoJS.mode.CBC
        });
        return f.toString()
    }
    function c(a, b, c) {
        var d, e;
        return setMaxDigits(131),
        d = new RSAKeyPair(b,"",c),
        e = encryptedString(d, a)
    }
    function d(d, e, f, g) {
        var h = {}
          , i = a(16);
        return h.encText = b(d, g),
        h.encText = b(h.encText, i),
        h.encSecKey = c(i, e, f),
        h
    }
    function e(a, b, d, e) {
        var f = {};
        return f.encText = c(a + e, b, d),
        f
    }
    window.asrsea = d,
    window.ecnonasr = e
    var c7f = NEJ.P
      , ev9m = c7f("nej.g")
      , v8n = c7f("nej.j")
      , k7d = c7f("nej.u")
      , Xs2x = c7f("nm.x.ek")
      , l7e = c7f("nm.x");
    if (v8n.bg8Y.redefine)
        return;
    window.GEnc = true;
    var brx0x = function(cxw4A) {
        var m7f = [];
        k7d.be8W(cxw4A, function(cxv4z) {
            m7f.push(Xs2x.emj[cxv4z])
        });
        return m7f.join("")
    };
    var cxt4x = v8n.bg8Y;
    v8n.bg8Y = function(Z8R, e7d) {
        var i7b = {}
          , e7d = NEJ.X({}, e7d)
          , me2x = Z8R.indexOf("?");
        if (window.GEnc && /(^|\.com)\/api/.test(Z8R) && !(e7d.headers && e7d.headers[ev9m.BL6F] == ev9m.Jm8e) && !e7d.noEnc) {
            if (me2x != -1) {
                i7b = k7d.gW0x(Z8R.substring(me2x + 1));
                Z8R = Z8R.substring(0, me2x)
            }
            if (e7d.query) {
                i7b = NEJ.X(i7b, k7d.fM0x(e7d.query) ? k7d.gW0x(e7d.query) : e7d.query)
            }
            if (e7d.data) {
                i7b = NEJ.X(i7b, k7d.fM0x(e7d.data) ? k7d.gW0x(e7d.data) : e7d.data)
            }
            i7b["csrf_token"] = v8n.gM0x("__csrf");
            Z8R = Z8R.replace("api", "weapi");
            e7d.method = "post";
            delete e7d.query;
            window.console.info(JSON.stringify(i7b))
            var bVj8b = window.asrsea(JSON.stringify(i7b), brx0x(["流泪", "强"]), brx0x(Xs2x.md), brx0x(["爱心", "女孩", "惊恐", "大笑"]));
            e7d.data = k7d.cx8p({
                params: bVj8b.encText,
                encSecKey: bVj8b.encSecKey
            })
        }
        cxt4x(Z8R, e7d)
    }
    ;
    v8n.bg8Y.redefine = true


    console.log(e7d.data);
}
)();

