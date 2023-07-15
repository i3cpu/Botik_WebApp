var app = new Vue({
    el: '.main',
    data: {

      showInfoBlock: true,
      showFormBlock: false,
      city_name:'', 
      city:'',
      tg:window.Telegram.WebApp,
      
    },
    methods: {
      to_form(){
        this.showFormBlock = true;
        this.showInfoBlock = false
      },
      close_webapp(){

        this.city=this.city_name;

        context = {
          city_name: this.city_name
        }

        this.tg.sendData(JSON.stringify(data));
        tg.close();
      }
    },
    watch: {
      city_name(newCity) {
        this.city = newCity; 
      }
    }
    
  });