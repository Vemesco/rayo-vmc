/* Copyright 2016 0k.io,ACSONE SA/NV
 *  * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl). */

odoo.define('vmc_hide_create_option.vmc_hide_create_option', function (require) {
    "use strict";
    var core = require('web.core'),
        data = require('web.data'),
        Dialog = require('web.Dialog'),
        relational_fields = require('web.relational_fields')
        
    var session = require('web.session');
    var _t = core._t,
        FieldMany2One = relational_fields.FieldMany2One

    function is_option_set (option) {
        if (_.isUndefined(option))
            return false;
        if (typeof option === 'string')
            return option === 'true' || option === 'True';
        if (typeof option === 'boolean')
            return option;
        return false
    };

    FieldMany2One.include({
        
        _search: function (search_val) {
            var self = this;
            var def = $.Deferred();
            this.orderer.add(def);

            // add options limit used to change number of selections record
            // returned.

            /*if (typeof this.nodeOptions.limit === 'number') {
                this.limit = this.nodeOptions.limit;
            }*/

            // add options field_color and colors to color item(s) depending on field_color value
            this.field_color = this.nodeOptions.field_color;
            this.colors = this.nodeOptions.colors;

            var context = this.record.getContext(this.recordParams);
            var domain = this.record.getDomain(this.recordParams);

            var blacklisted_ids = this._getSearchBlacklist();
            if (blacklisted_ids.length > 0) {
                domain.push(['id', 'not in', blacklisted_ids]);
            }

            this._rpc({
                model: this.field.relation,
                method: "name_search",
                kwargs: {
                    name: search_val,
                    args: domain,
                    operator: "ilike",
                    limit: this.limit + 1,
                    context: context,
                }
            }).then(function (result) {
                // possible selections for the m2o
                var values = _.map(result, function (x) {
                    x[1] = self._getDisplayName(x[1]);
                    return {
                        label: _.str.escapeHTML(x[1].trim()) || data.noDisplayContent,
                        value: x[1],
                        name: x[1],
                        id: x[0],
                    };
                });

                // Search result value colors
                if (self.colors && self.field_color) {
                    var value_ids = [];
                    for (var index in values) {
                        value_ids.push(values[index].id);
                    }
                    self._rpc({
                        model: self.field.relation,
                        method: 'search_read',
                        fields: [self.field_color],
                        domain: [['id', 'in', value_ids]]
                    }).then(function (objects) {
                        for (var index in objects) {
                            for (var index_value in values) {
                                if (values[index_value].id == objects[index].id) {
                                    // Find value in values by comparing ids
                                    var value = values[index_value];
                                    // Find color with field value as key
                                    var color = self.colors[objects[index][self.field_color]] || 'black';
                                    value.label = '<span style="color:' + color + '">' + value.label + '</span>';
                                    break;
                                }
                            }
                        }
                        def.resolve(values);
                    })

                }

                values = values.slice(0, self.limit);     
                values.push({
                    label: _t("Search More..."),
                    action: function () {
                        self._rpc({
                                model: self.field.relation,
                                method: 'name_search',
                                kwargs: {
                                    name: search_val,
                                    args: domain,
                                    operator: "ilike",
                                    limit: 80,
                                    context: context,
                                },
                            })
                            .then(self._searchCreatePopup.bind(self, "search"));
                    },
                    classname: 'o_m2o_dropdown_option',
                });
                
                // create and edit ...
                
                session.user_has_group('vmc_hide_create_option.group_hide_create_option').then(function(has_group) {
                if (has_group){
                    var createAndEditAction = function () {
                        // Clear the value in case the user clicks on discard
                        self.$('input').val('');
                        return self._searchCreatePopup("form", false, self._createContext(search_val));
                    };
                    values.push({
                        label: _t("Create and Edit..."),
                        action: createAndEditAction,
                        classname: 'o_m2o_dropdown_option',
                    });
                    values.push({
                        label: _.str.sprintf(_t('Create "<strong>%s</strong>"'),
                            $('<span />').text(search_val).html()),
                        action: self._quickCreate.bind(self, search_val),
                        classname: 'o_m2o_dropdown_option'
                    });
                }else if (values.length === 0) {
                    values.push({
                        label: _t("No results to show..."),
                    });
                }
            });
                // Check if colors specified to wait for RPC
                if (!(self.field_color && self.colors)) {
                    def.resolve(values);
                }
            });

            return def;
        },
    });

});
