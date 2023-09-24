from openupgradelib import openupgrade


@openupgrade.migrate(use_env=False)
def migrate(cr, version):

    openupgrade.logged_query(cr, """
        ALTER TABLE product_product
        ADD COLUMN resource_booking_type_id int4,
        ADD COLUMN resource_booking_type_combination_rel_id int4;
    """)
    openupgrade.logged_query(cr, """
        UPDATE product_product p
        SET
            resource_booking_type_id = t.resource_booking_type_id,
            resource_booking_type_combination_rel_id =
                t.resource_booking_type_combination_rel_id
        FROM product_template as t
        WHERE p.product_tmpl_id = t.id;
    """)
