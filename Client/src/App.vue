<template>
  <div class="container">
    <div class="row">
      <div class="col-md-6">
        <div class="card">
          <div class="card-body">
            <h2 class="card-title">Ingredients</h2>
            <ul class="list-group">
              <li v-for="ingredient in ingredients" :key="ingredient.id" class="list-group-item">
                {{ ingredient.name }}
                <button @click="removeIngredient(ingredient.id)" class="btn btn-danger btn-sm float-right">Remove</button>
              </li>
            </ul>
            <div class="input-group mt-3">
              <input v-model="newIngredient" @keyup.enter="addIngredient" placeholder="Add an ingredient" class="form-control">
              <div class="input-group-append">
                <button @click="addIngredient" class="btn btn-primary">Add</button>
              </div>
            </div>
            <button @click="removeAllIngredients" class="btn btn-danger mt-3">Remove All</button>
          </div>
        </div>
      </div>
      <div class="col-md-6">
        <div class="card">
          <div class="card-body">
            <h2 class="card-title">Menu Options</h2>
            <ul class="list-group">
              <li v-for="option in menuOptions" :key="option.id" class="list-group-item">
                {{ option.name }}
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      ingredients: [], // Store the list of ingredients
      newIngredient: "", // Input field for adding new ingredients
      menuOptions: [
        { id: 1, name: "Option 1" },
        { id: 2, name: "Option 2" },
        // Add more menu options as needed
      ],
    };
  },
  methods: {
    addIngredient() {
      if (this.newIngredient.trim() !== "") {
        this.ingredients.push({ id: Date.now(), name: this.newIngredient });
        this.newIngredient = "";
      }
    },
    removeIngredient(id) {
      this.ingredients = this.ingredients.filter((ingredient) => ingredient.id !== id);
    },
    removeAllIngredients() {
      this.ingredients = [];
    },
  },
};
</script>

<style scoped>
/* You can add custom CSS styles here if needed */
</style>
