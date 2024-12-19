<template>
    <div>
      <div>
  
        {{ spotlocation }}
  
      </div>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      spotlocation: {
        type: Array,
        required: true,
      },
    },
  }
  </script>

  