/**
 * GeneticSoylent should be initialized with a target nutrient profile and a list of ingredients.
 */

var GeneticSoylent = function(opts) {
    opts = opts || {};

    this.populationSize = opts.populationSize || 100;
    this.mutationProbability = opts.mutationProbability || 0.7;
    this.mutationMultiplier = opts.mutationMultiplier || 0.1;
    this.deathRate = opts.deathRate || 0.3;

    this.ingredients = opts.ingredients;
    this.targetNutrients = opts.targetNutrients;

    this.ratios = this.defaultRatios();

//For test
    //alert("Numerator: " + this.ratios['Omega-6:Omega-3']['numerator']);
    //alert("Numerator: " + this.ratios['Soy Lecithin Granules:Sea Sal']['numerator']);
    //alert(this.recipes[0].ingredientAmounts[0]);
    //alert(this.recipes[0].ingredientAmounts[1]);
    //alert("Denominator: " + this.ratios['Omega-6:Omega-3']['denominator']);
    //alert("Denominator: " + this.ratios['Soy Lecithin Granules:Sea Sal']['denominator']);

    this.reset();
};

/**
 * Randomly generate new recipes. The number of recipes to generate is defined by populationSize
 */
GeneticSoylent.prototype.reset = function() {
    this.currentGeneration = 0;
    this.recipes = [];
    this.recipes.push(new Recipe(this, _.map(this.ingredients, function() { return 1; })));
    for (var i = 1; i < this.populationSize; i++){
        this.recipes.push(new Recipe(this));
    }
};

GeneticSoylent.prototype.nextGeneration = function() {

    // Throw out the worst performing recipes. The % thrown out is defined by the deathRate variable.
    var recipesToKeep = Math.floor(this.recipes.length * (1 - this.deathRate));
    this.recipes = this.recipes.slice(0, recipesToKeep);

    // Pick two random recipes from the remaining list and 'mate' them, to produce a child recipe.
    for (var popIndex = 0; this.recipes.length < this.populationSize; popIndex++) {
        var parentOne = this.recipes[Math.floor(Math.random() * recipesToKeep)];
        var parentTwo = this.recipes[Math.floor(Math.random() * recipesToKeep)];
        var childRecipe = parentOne.createChildWith(parentTwo);

        //childRecipe
        this.recipes.push(childRecipe);
    }

    this.sortRecipes();
    this.currentGeneration++;
    this.render();
    //TODO
/**
 * if currentGeneration is greater than 200, force it stop, and show the continue button.
 *
 *
 */
    if(this.currentGeneration > 100){
        $('.calculating').hide();
        $('.nutrient-label').show();
        $('.submit').show();
        testGeneticSoylent.autoGenerate = false;
        $('.pause-genetic-algorithm').hide();
        $('.start-genetic-algorithm').show();
        $('.hahahahaha').hide();
        $('.sasasasasa').show();
    }

    if (this.autoGenerate) {
        var self = this;
        setTimeout(function() {
            self.nextGeneration();
        }, 100);
    }
};

/**
 * Sort the recipes from best to worst
 */
GeneticSoylent.prototype.sortRecipes = function(a, b) {
    this.recipes.sort(function(a, b) {
        if (b.completenessScore < a.completenessScore) {
            return -1;
        }
        else if (a.completenessScore < b.completenessScore) {
            return 1;
        }
        else {
            return 0;
        }
    });
};

GeneticSoylent.prototype.defaultRatios = function() {

    /*
    if(this.recipes[0].ingredientAmounts != null){

      var n = render().ingredientHtml.recipes[0].ingredientAmounts;
      var d = render().ingredientHtml.recipes[0].ingredientAmounts;
    }
    else{
  */
      //var n = this.ingredients[0]["amount"];
      //var d = this.ingredients[1]["amount"];
    //}
    return {
       //'Calcium:Phosphorus': {min: 1, max: 2.5, numerator: "calcium", denominator: "phosphorus", unitCorrection: 1, importanceFactor: 1},
       //'Calcium:Magnesium':  {min: 1, max: 2, numerator: "calcium", denominator: "magnesium", unitCorrection: 1000, importanceFactor: 1},
       //'Potassium:Sodium':  {min: 2, max: 999, numerator: "potassium", denominator: "sodium", unitCorrection: 1, importanceFactor: 1},
       //'Iron:Copper':  {min: 10, max: 17, numerator: "iron", denominator: "copper", unitCorrection: 1, importanceFactor: 1},
       //'Zinc:Copper':  {min: 10, max: 15, numerator: "zinc", denominator: "copper", unitCorrection: 1, importanceFactor: 1},
       //'Iron:Zinc':  {min: 0.01, max: 2, numerator: "iron", denominator: "zinc", unitCorrection: 1, importanceFactor: 1},
       'Omega-6:Omega-3':  {min: 1, max: 2.31, numerator: "omega_6", denominator: "omega_3", unitCorrection: 1, importanceFactor: 1},
       //'Soy Lecithin Granules:Sea Sal':  {min: 0.0005, max: 777, numerator: this.ingredients[0]["amount"], denominator: this.ingredients[1]["amount"], unitCorrection: 1, importanceFactor: 1},
       //'Soy Lecithin Granules:Sea Sal':  {min: 0.0005, max: 777, numerator: n, denominator: d, unitCorrection: 1, importanceFactor: 1},
    };
};


GeneticSoylent.prototype.render = function() {

    var ingredientHtml = _.template([
      '<% var orderedIngredients = [] %>',
      '<% _.each(ingredients, function(ingredient, idx) { %>',
        '<% orderedIngredients.push([ ingredient.name, Math.round(amounts[idx]) ]) %>',
      '<% }); %>',
      '<div class="orderedIngredients">',

        '<% orderedIngredients.sort(function(a, b) { %>',
          '<% if (a[1] === b[1]) { %>',
            '<% return 0 %>',
          '<% } else { %>',
            '<% return (a[1] > b[1]) ? -1 : 1 %>',
          '<% } %>',
        '<% }); %>',

        'Ingredients: ',
        '<% _.each(orderedIngredients, function(ingredient, idx) { %>',
          '<%= ingredient[0] %>, ',
        '<% }); %>',
      '</div>',
    ].join(''));
/**************************** TO SHOW DEVIATION **********************************/
    var deviationHtml = _.template('<%= -completenessScore.toFixed(1) %>');

    //alert(deviationHtml);

    $('#deviationTable').html(deviationHtml({
        total: this.recipes[0].nutrientTotals,
        amounts: this.recipes[0].ingredientAmounts,
        ingredients: this.ingredients,
        targetProfile: this.targetNutrients,
        completenessScore: this.recipes[0].completenessScore,
        nutrientCompleteness: this.recipes[0].nutrientCompleteness,
        nutrientKeys: _.keys(this.targetNutrients)
    }));
/**
 * if Deviation is 0, show the submit button.
 *
 *
 */
    if(this.recipes[0].completenessScore == 0){
        $('.calculating').hide();
        $('.nutrient-label').show();
        $('.submit').show();

        testGeneticSoylent.autoGenerate = false;
        $('.pause-genetic-algorithm').hide();
        $('.start-genetic-algorithm').show();
        $('.hahahahaha').hide();
        $('.sasasasasa').show();
    }
/*
    $('#deviationTable').val(function(){

        //var jsonToRun = $.parseJSON(this.value);
        //alert(this.value);

        $('.submit').show();
    });
*/
/*********************************************************************/
    var nutrientHtml = _.template([
      '<table class="table table-condensed">',
        '<tr>',
          '<th class="text-left">Nutrient</th>',
          '<th class="text-center">Min</th>',
          '<th class="text-center">Amount</th>',
          '<th class="text-center">Max</th>',
          '<th class="text-center">% Deviation</th>',
          '<th class="text-center">Priority</th>',
        '</tr>',
        '<% _.each(nutrientKeys, function(nutrient, index) { %>',
          '<% if(total[nutrient] != undefined){ %>',
            '<% var classCompleteness = ""; %>',
            // '<% console.log(nutrient + ": " + classCompleteness) %>',
            '<% if(!nutrientCompleteness[nutrient]) { classCompleteness = "success"; } else { classCompleteness = "danger"; } %>',
            '<tr class="<%= classCompleteness %>">',
              '<th class="text-left"><%= nutrient %></th>',
              '<td class="text-center"><input name="<%= nutrient %>_._min" class="nutrientInput" value="<%= targetProfile[nutrient].min %>"></input></td>',
              '<% var tooltip = "" %>',
              '<% _.each(ingredients, function(ingredient, idx) { %>',
                '<% tooltip += (ingredient[nutrient] * Math.round(amounts[idx])).toFixed(2) + "\t" + ingredient["name"] + "\\r" %>',
              '<% }); %>',
              '<td class="text-center" title="<%= tooltip %>"><%= total[nutrient].toFixed(2) %></td>',
              '<td class="text-center"><input name="<%= nutrient %>_._max" class="nutrientInput" value="<%= targetProfile[nutrient].max %>"></input></td>',
              '<td class="text-center"><%= nutrientCompleteness[nutrient].toFixed(1) %>%</td>',
              '<td class="text-center"><input name="<%= nutrient %>_._importanceFactor" class="nutrientInput" value="<%= targetProfile[nutrient].importanceFactor %>"></input>',
            '</tr>',
          '<% }; %>',
        '<% }); %>',

        //ratioCompleteness
        '<% if(typeof ratioKeys != "undefined"){ %>',
          '<% _.each(ratioKeys, function(theRatio, index) { %>',
              '<% var classCompleteness = ""; %>',
              // '<% console.log(nutrient + ": " + classCompleteness) %>',
              '<% if(!ratioCompleteness[theRatio]) { classCompleteness = "success"; } else { classCompleteness = "danger"; } %>',
              '<tr class="<%= classCompleteness %>">',
                '<th class="text-left"><%= theRatio %></th>',
                '<td class="text-center"><input name="<%= theRatio %>_._min" class="ratioInput" value="<%= targetRatios[theRatio].min %>"></input></td>',
                '<td class="text-center"><%= ratioAmounts[theRatio].toFixed(2) %></td>',
                '<td class="text-center"><input name="<%= theRatio %>_._max" class="ratioInput" value="<%= targetRatios[theRatio].max %>"></input></td>',
                '<td class="text-center"><%= ratioCompleteness[theRatio].toFixed(1) %>%</td>',
                '<td class="text-center"><input name="<%= theRatio %>_._importanceFactor" class="ratioInput" value="<%= targetRatios[theRatio].importanceFactor %>"></input>',
              '</tr>',
          '<% }); %>',
        '<% }; %>',


      '</table>'
    ].join(''));

    $('#ingredientTable').html(ingredientHtml({
        total: this.recipes[0].nutrientTotals,
        amounts: this.recipes[0].ingredientAmounts,
        ingredients: this.ingredients,
        targetProfile: this.targetNutrients,
        completenessScore: this.recipes[0].completenessScore,
        nutrientCompleteness: this.recipes[0].nutrientCompleteness,
        nutrientKeys: _.keys(this.targetNutrients)
    }));

    // specify the nutrient keys we want in the second column
    var nutrientTableKeysForFirstColumn = [
        "cost",
        "calories",
        "carbs",
        "protein",
        "fat",
        "omega_3",
        "omega_6",
        "fiber",
        "vitamin_a",
        "vitamin_b6",
        "vitamin_b12",
        "vitamin_c",
        "vitamin_d",
        "vitamin_e",
        "vitamin_k"
    ];

    // put all other nutrient keys into the third column
    var nutrientTableKeysForSecondColumn = _.keys(this.targetNutrients);
    nutrientTableKeysForSecondColumn = $.grep(nutrientTableKeysForSecondColumn, function(value){
      return $.inArray(value, nutrientTableKeysForFirstColumn) + 1;
    }, true);

    $('#nutrientTable').html(nutrientHtml({
        total: this.recipes[0].nutrientTotals,
        amounts: this.recipes[0].ingredientAmounts,
        ingredients: this.ingredients,
        targetProfile: this.targetNutrients,
        nutrientCompleteness: this.recipes[0].nutrientCompleteness,
        //nutrientKeys: _.keys(this.targetNutrients)
        nutrientKeys: nutrientTableKeysForFirstColumn,

        ratioKeys: _.keys(this.recipes[0].ratioCompleteness),
        ratioCompleteness: this.recipes[0].ratioCompleteness,
        ratioAmounts: this.recipes[0].ratioAmounts,
        targetRatios: this.ratios,
    }));
    $('#nutrientTableRemainder').html(nutrientHtml({
        total: this.recipes[0].nutrientTotals,
        amounts: this.recipes[0].ingredientAmounts,
        ingredients: this.ingredients,
        targetProfile: this.targetNutrients,
        nutrientCompleteness: this.recipes[0].nutrientCompleteness,
        nutrientKeys: nutrientTableKeysForSecondColumn.sort()
    }));


    var ingredientHtmlJson = _.template([
        '{',
        '<br>',
        '<% _.each(ingredients, function(ingredient, idx) { %>',
            '&nbsp;&nbsp;"<%= ingredient.name %>"',
            ': ',
            '<%= Math.round(amounts[idx]) %>',
            ',',
            '<br>',
        '<% }); %>',
        '}'
    ].join(''));

    $('#ingredientTableJson').html(ingredientHtmlJson({
        total: this.recipes[0].nutrientTotals,
        amounts: this.recipes[0].ingredientAmounts,
        ingredients: this.ingredients,
        targetProfile: this.targetNutrients,
        completenessScore: this.recipes[0].completenessScore,
        nutrientCompleteness: this.recipes[0].nutrientCompleteness,
        nutrientKeys: _.keys(this.targetNutrients)
    }));

    var ingredientHtmlJsonVal = _.template([
        '{',
        '<% _.each(ingredients, function(ingredient, idx) { %>',
            '"<%= ingredient.name %>"',
            ': ',
            '<%= Math.round(amounts[idx]) %>',
            ',',
        '<% }); %>',
        '}'
    ].join(''));

    $('#ingredientTableJsonVal').text(ingredientHtmlJsonVal({
        total: this.recipes[0].nutrientTotals,
        amounts: this.recipes[0].ingredientAmounts,
        ingredients: this.ingredients,
        targetProfile: this.targetNutrients,
        completenessScore: this.recipes[0].completenessScore,
        nutrientCompleteness: this.recipes[0].nutrientCompleteness,
        nutrientKeys: _.keys(this.targetNutrients)
    }));
/*****************************Json file of complete nutrients*****************************/
    var nutrientHtmlJsonVal = _.template([
        '{',
            '<% _.each(nutrientKeys, function(nutrient, index) { %>',
              '<% if(total[nutrient] != undefined){ %>',
                  '"<%= nutrient %>"',
                  ': ',
                  '<% var tooltip = "" %>',
                  '<% _.each(ingredients, function(ingredient, idx) { %>',
                    '<% tooltip += (ingredient[nutrient] * Math.round(amounts[idx])).toFixed(2) + "\t" + ingredient["name"] + "\\r" %>',
                  '<% }); %>',
                  '<%= total[nutrient].toFixed(2) %>',
                  ',',
              '<% }; %>',
            '<% }); %>',
        '}'
        ].join(''));

    $('#nutrientHtmlJson').html(nutrientHtmlJsonVal({
        total: this.recipes[0].nutrientTotals,
        amounts: this.recipes[0].ingredientAmounts,
        ingredients: this.ingredients,
        targetProfile: this.targetNutrients,
        nutrientCompleteness: this.recipes[0].nutrientCompleteness,
        //nutrientKeys: _.keys(this.targetNutrients)
        nutrientKeys: nutrientTableKeysForFirstColumn,

        ratioKeys: _.keys(this.recipes[0].ratioCompleteness),
        ratioCompleteness: this.recipes[0].ratioCompleteness,
        ratioAmounts: this.recipes[0].ratioAmounts,
        targetRatios: this.ratios,
    }));
    $('#nutrientHtmlJson2').html(nutrientHtmlJsonVal({
        total: this.recipes[0].nutrientTotals,
        amounts: this.recipes[0].ingredientAmounts,
        ingredients: this.ingredients,
        targetProfile: this.targetNutrients,
        nutrientCompleteness: this.recipes[0].nutrientCompleteness,
        nutrientKeys: nutrientTableKeysForSecondColumn.sort()
    }));
/************************************************************/


    $('.nutrientInput').change(function(){
        // split the name of the function by separator "_._"
        // keyInfo[0] is the nutrient name
        // keyInfo[1] is the name of the value for that nutrient
        var keyInfo = this.name.split("_._");
        testGeneticSoylent.targetNutrients[keyInfo[0]][keyInfo[1]] = this.value;
    });

    $('.ratioInput').change(function(){
        // split the name of the function by separator "_._"
        // keyInfo[0] is the nutrient name
        // keyInfo[1] is the name of the value for that nutrient
        var keyInfo = this.name.split("_._");
        testGeneticSoylent.ratios[keyInfo[0]][keyInfo[1]] = this.value;
    });

    $('.ingredientInput').change(function(){
        var keyInfo = this.name.split("_._");
        testGeneticSoylent.ingredients[keyInfo[0]][keyInfo[1]] = +this.value;
    });

    $('.generation').val(this.currentGeneration);

};
