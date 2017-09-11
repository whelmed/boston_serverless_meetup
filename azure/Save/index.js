module.exports = function (context, req) {
    context.log('JavaScript HTTP trigger function processed a request.');

    
    if (req.body && req.body.content && req.body.header) {

        context.bindings.outputDoc = JSON.stringify({
            "content": req.body.content,
            "created": new Date().toString(),
            "header": req.body.header    
        });
        context.res = {
            // status: 200, /* Defaults to 200 */
            body: context.bindings.outputDoc
        };
    }
    else {
        context.res = {
            status: 400,
            body: { "error": "Content or header fields are missing in posted JSON"}
        };
    }
    context.done();
};