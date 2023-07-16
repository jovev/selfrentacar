// rent_signature.js

odoo.define('rent_signature', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var core = require('web.core');
    var session = require('web.session');

    var _t = core._t;

    FormController.include({
        renderButtons: function ($node) {
            this._super.apply(this, arguments);

            if (this.$buttons) {
                var self = this;

                this.$buttons.on('click', '.o_rent_signature_clear_signature', function () {
                    self._clearSignature();
                });

                this.$buttons.on('click', '.o_rent_signature_save_signature', function () {
                    self._saveSignature();
                });
            }
        },

        _clearSignature: function () {
            var self = this;
            this.renderer.state.data.signature = false;
            this.renderer.update();
        },

        _saveSignature: function () {
            var self = this;
            var signatureData = document.getElementById('signature_canvas').toDataURL();

            session.rpc('/rent_signature/save_signature', {
                'id': this.renderer.state.data.id,
                'signature': signatureData,
            }).then(function () {
                self._clearSignature();
            });
        },
    });
});
