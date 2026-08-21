module.exports = function(eleventyCc) {
    eleventyCc.addPassthroughCopy("src/assets");
    return {
        
         //htmlTemplateEngine: false,
        //markdownTemplateEngine: false,
       htmlTemplateEngine: "njk",
        markdownTemplateEngine: "njk",
        
        dir: {
            input: "src",
            output: "_site"
        }
    };
};
