/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./templates/**/*.{html,js}"],
  theme: {
    extend: {
        animation:{
            colorchangeWhitetoPurple : 'colorchangeWhitetoPurple 4s ease-in-out infinite',
            colorchangePurpletoWhite :'colorchangePurpletoWhite 4s ease-in-out infinite',

        },
        keyframes:{
            colorchangeWhitetoPurple:{
                '0%': {backgroundColor:'white'},
                '25%':{backgroundColor:'purple'},
                  '75%': {backgroundColor:'white'},
                '100%':{backgroundColor:'purple'}
            },
            colorchangePurpletoWhite:{
               '0%': {backgroundColor:'purple'},
                '25%':{backgroundColor:'white'},
                '75%': {backgroundColor:'purple'},
                '100%':{backgroundColor:'white'},

            },

        }
    },
  },
  plugins: [],
}

