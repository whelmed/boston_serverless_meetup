// Imports the Google Cloud client library
const Datastore = require('@google-cloud/datastore');
const uuid = require('uuid');

// Instantiates a client
const datastore = Datastore();

// The kind for the new entity
const kind = 'Tweet';

/**
 * Responds to any HTTP request that can provide a "message" field in the body.
 *
 * @param {!Object} req Cloud Function request context.
 * @param {!Object} res Cloud Function response context.
 */
exports.api = function api(req, res) {
    res.set('Access-Control-Allow-Origin', "*");
    res.set('Access-Control-Allow-Methods', 'GET, POST');
    res.set('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept');

    switch (req.method) {
        case 'GET':
            get(function (err, entities) {
                if (err) {
                    res.status(500).send({ error: err });
                }
                res.status(200).send(entities);
            });
            break;
        case 'POST':
            save(req.body, function (err, data) {
                if (err) {
                    res.status(500).send({ error: err });
                }
                res.status(200).send(data);
            });
            break;
        case 'OPTIONS':
            res.status(200).end();
            break;
        default:
            res.status(500).send({ error: 'Something blew up!' });
            break;
    }
};


function get(callback) {
    var query = datastore.createQuery(kind);
    datastore.runQuery(query, function (err, entities) {
        return callback(err, entities);
    });
}

function save(body, callback) {
    // The name/ID for the new entity
    var name = uuid.v4();

    // The Cloud Datastore key for the new entity
    const taskKey = datastore.key([kind, name]);

    // Prepares the new entity
    const task = {
        key: taskKey,
        data: {
            content: body.content,
            header: body.header,
            created: new Date().toString(),
        }
    };

    // Saves the entity
    datastore.save(task)
        .then(() => {
            callback(null, task.data);
        })
        .catch((err) => {
            console.error('ERROR:', err);
            callback(err, null);
        });
}
