// -*- coding: utf-8; -*-
Vue.component("detail-modal", {
  template: "#detail-modal",
  props: {
    index: Number,
    results: Object
  },
  data: function() {
    return this.results[this.index];
  }
});

var app = new Vue({
  el: "#app",
  data: {
    isActive: "1",

    regist_isbn: "",

    isbn: "",
    title: "",
    publisher: "",
    pubdate: "",
    cover: "",
    author: "",

    search_clicked: 0,

    results: []
  },
  methods: {
    regist: function() {
      if (this.regist_isbn.length == 0) {
        alert("ISBNコードが入力されていません");
        return;
      }
      // this.$el.querySelector("#container").style.display = "block"
      let text = this.regist_isbn.replace(/-/g, "");
      let url = "/regist?isbn=" + text;

      console.log(url);
      axios.get(url).then(response => {
        console.log(response);

        if (response.data.length == 0) {
          alert("登録できませんでした（GoogleBooksに見つかりませんでした）");
          return;
        }

        // let results_old = this.results
        // this.results = []
        // // for( let value of response.data) {
        // //     this.results.push( value )
        // // }
        // this.results.push(response.data)
        // //					app.$forceUpdate();
        // if (results_old == this.results) {
        //     window.scrollTo(0, document.body.scrollHeight - this.$el.querySelector("#container").clientHeight);
        //     this.search_clicked = 0
        // } else {
        //     this.search_clicked = 1
        // }
      });
    },

    search: function() {
      // 検索option
      let search_option = [];

      if (this.isbn.length != 0) {
        search_option.push("isbn=" + this.isbn);
      }
      if (this.title.length != 0) {
        search_option.push("title=" + this.title);
      }
      if (this.publisher.length != 0) {
        search_option.push("publisher=" + this.publisher);
      }
      if (this.pubdate.length != 0) {
        search_option.push("pubdate=" + this.pubdate);
      }
      if (this.cover.length != 0) {
        search_option.push("cover=" + this.cover);
      }
      if (this.author.length != 0) {
        search_option.push("author=" + this.author);
      }

    //   if (search_option.length == 0) {
    //     // 採用カウントが 0 の場合:
    //     alert("検索条件を設定してください");
    //     return;
    //   }
      console.log("aaaa");

      let search_str = search_option.join("&");
      // this.$el.querySelector("#container").style.display = "block"

      let url = "/search?" + search_str;
      let url2 = url.replace(/#/g, "%23").replace(/\+/g, "%2b");
      console.log(url2);
      axios.get(url2).then(response => {
        console.log(response);

        let results_old = this.results;
        this.results = [];
        for (let value of response.data) {
          this.results.push(value);
        }
        //					app.$forceUpdate();
        if (results_old == this.results) {
          if (this.$el.querySelector("#container") != null) {
            window.scrollTo(
              0,
              document.body.scrollHeight -
                this.$el.querySelector("#container").clientHeight
            );
          }
          this.search_clicked = 0;
        } else {
          if (this.results == []) {
            this.search_clicked = 0;
          } else {
            this.search_clicked = 1;
          }
        }
      });
    },
    isSelect: function(num) {
      this.isActive = num;
    },

    list: function() {
      let url = "/list";
      console.log(url);
      axios.get(url).then(response => {
        console.log(response);

        let results_old = this.results;
        this.results = [];
        for (let value of response.data) {
          this.results.push(value);
        }
        //	app.$forceUpdate();
        if (results_old == this.results) {
          if (this.$el.querySelector("#container") != null) {
            window.scrollTo(
              0,
              document.body.scrollHeight -
                this.$el.querySelector("#container").clientHeight
            );
          }
          this.search_clicked = 0;
        } else {
          if (this.results == []) {
            this.search_clicked = 0;
          } else {
            this.search_clicked = 1;
          }
        }
      });
    }
  },
  updated: function() {
    this.$nextTick(function() {
      if (this.search_clicked == 1) {
        if (this.$el.querySelector("#container") != null) {
          window.scrollTo(
            0,
            document.body.scrollHeight -
              this.$el.querySelector("#container").clientHeight
          );
        }
        this.search_clicked = 0;
      }
    });
  }
});
