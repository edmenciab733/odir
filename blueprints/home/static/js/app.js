Vue.use(Buefy)
Vue.prototype.$axios = axios;



const vm = new Vue({ // Again, vm is our Vue instance's name for consistency.
  el: '#app',
  delimiters: ['[[', ']]'],
  data: {
  
    dropFiles: [],  
    fileShow: true, 
    image: null, diagnostico: [], diagnosticoMensaje: "Escanear imagen...", isLoading: false,
    isFullPage: true
    
  },
  mounted() {
    console.log("init")
    
    
    
  },
  methods: {
    obtenerDiagnostico()
    { 
      Swal.fire({
        title: "Esta imagen será escaneada. Desea continuar?",
        showCancelButton: true,
        confirmButtonText: 'Sí',
        cancelButtonText: `Cancelar`,
    
      }).then((result) => {
        
        if (result.isConfirmed) { 
          const formData = new FormData();
          formData.append('file', this.dropFiles[0]);
          const headers = { 'Content-Type': 'multipart/form-data' };
          this.isLoading = true
          this.diagnosticoMensaje = "Diagnosticando..."
          this.diagnostico = [];
          axios.post('/inferencia', formData, { headers }).then((res) => {
              this.diagnosticoMensaje = "";
              
              for (const [key, value] of Object.entries(res.data)) {
                let data =  { diagnostico: key , probabilidad: value };
                this.diagnostico.push(data);

              }
              if(this.diagnostico.length == 0)
              {
                this.diagnosticoMensaje = "No hay diagnostico posible"
              }
              this.isLoading = false
          });
        } 
      }); 
      
    },
    deleteDropFile(index) {
        this.dropFiles.splice(index, 1);
        this.diagnostico = [];
        this.diagnosticoMensaje = "Escanear imagen..."
    }, 
    async fileChangeHandler(val) {      
      this.image = await new Promise(resolve=>{ 
       const reader = new FileReader()
       let file = val[0];
       reader.onload = (e) => {
            resolve(e.target.result)
          }
        reader.readAsDataURL(file);
      });
     
    }
  },
  watch: {
    dropFiles: function(val) {
        //do something when the data changes.
        if (val.length > 0) {
            this.fileShow = false
            this.fileChangeHandler(val) 
           

            
        }else
        {
          this.fileShow = true
          this.image = null
          
        }
    }
}
})