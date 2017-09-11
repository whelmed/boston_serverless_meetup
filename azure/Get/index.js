module.exports = function (context, req) {

    var docs = context.bindings.inputDoc;
  
    context.res = {
        // status: 200, /* Defaults to 200 */
        body: docs
    };

    context.done();
};