const { createApp } = Vue
    createApp({
        data() {
            return {
                dramas:[],
                //url:'http://localhost:5000/dramas',
                // si el backend esta corriendo local usar localhost 5000(si no lo subieron a pythonanywhere)
                url:'https://astorniolo.pythonanywhere.com/dramas',   //url:'http://mcerda.pythonanywhere.com/dramas', // si ya lo subieron a pythonanywhere
                error:false,
                cargando:true,
                /*atributos para el guardar los valores del formulario */
                id:0,
                titulo:"",
                episodios:0,
                genero:"",
                autor:"",
                imagen:"",
                anio:0,
                estrellas:0,
                descripcion:"",
            }
        },
        methods: {
            fetchData(url) {
                fetch(url)
                    .then(response => response.json())
                    .then(data => {
                        this.dramas = data;
                        this.cargando=false
                    })
                    .catch(err => {
                        console.error(err);
                        this.error=true
                    })
            },

            eliminar(drama) {
                const url = this.url+'/' + drama;
                var options = {
                    method: 'DELETE',
                }
                fetch(url, options)
                    .then(res => res.text()) // or res.json()
                    .then(res => {
                        location.reload();
                    })
            },

            grabar(){
                let drama = {
                    titulo:this.titulo,
                    episodios:this.episodios,
                    genero:this.genero,
                    autor:this.autor,
                    imagen:this.imagen,
                    anio:this.anio,
                    estrellas:this.estrellas,
                    descripcion:this.descripcion
                }
                var options = {
                    body:JSON.stringify(drama),
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    redirect: 'follow'
                }
                fetch(this.url, options)
                    .then(function () {
                        alert("Registro grabado")
                        window.location.href = "./dramas.html";
                    })
                    .catch(err => {
                        console.error(err);
                        alert("Error al Grabarr")
                    })
            }
        },
        created() {
            this.fetchData(this.url)
        },
}).mount('#app')