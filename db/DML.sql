\copy "region"     from './data/region.csv'        DELIMITER '|' CSV;
\copy "nation"     from './data/nation.csv'        DELIMITER '|' CSV;
\copy "customer"   from './data/customer.csv'    DELIMITER '|' CSV;
\copy "supplier"   from './data/supplier.csv'    DELIMITER '|' CSV;
\copy "part"       from './data/part.csv'            DELIMITER '|' CSV;
\copy "partsupp"   from './data/partsupp.csv'    DELIMITER '|' CSV;
\copy "orders"     from './data/orders.csv'        DELIMITER '|' CSV;
\copy "lineitem"   from './data/lineitem.csv'    DELIMITER '|' CSV;