CREATE TABLE IF NOT EXISTS public.region
(
	r_regionkey integer NOT NULL,
	r_name character(25) COLLATE pg_catalog."default" NOT NULL,
	r_comment character varying(152) COLLATE pg_catalog."default",
	CONSTRAINT region_pkey PRIMARY KEY (r_regionkey)
)
WITH (
	OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.region
	OWNER to postgres;



CREATE TABLE IF NOT EXISTS public.nation
(
	n_nationkey integer NOT NULL,
	n_name character(25) COLLATE pg_catalog."default" NOT NULL,
	n_regionkey integer NOT NULL,
	n_comment character varying(152) COLLATE pg_catalog."default",
	CONSTRAINT nation_pkey PRIMARY KEY (n_nationkey),
	CONSTRAINT fk_nation FOREIGN KEY (n_regionkey)
		REFERENCES public.region (r_regionkey) MATCH SIMPLE
		ON UPDATE NO ACTION
)
WITH (
	OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.nation
	OWNER to postgres;



CREATE TABLE IF NOT EXISTS public.part
(
	p_partkey integer NOT NULL,
	p_name character varying(55) COLLATE pg_catalog."default" NOT NULL,
	p_mfgr character(25) collate pg_catalog."default" not null,
	p_brand character(10) collate pg_catalog."default" not null,
	p_type character varying(25) collate pg_catalog."default" not null,
	p_size integer not null,
	p_container character(10) collate pg_catalog."default" not null,
	p_retailprice numeric(15,2) not null,
	p_comment character varying(23) collate pg_catalog."default" not null,
	constraint part_pkey primary key (p_partkey)
)
WITH (
	OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.part
	OWNER to postgres;



CREATE TABLE IF NOT EXISTS public.supplier
(
	s_suppkey integer NOT NULL,
	s_name character(25) COLLATE pg_catalog."default" NOT NULL,
	s_address character varying(40) COLLATE pg_catalog."default" not null,
	s_nationkey integer not null,
	s_phone character(15) COLLATE pg_catalog."default" NOT NULL,
	s_acctbal numeric(15,2) not null,
	s_comment character varying(101) COLLATE pg_catalog."default" NOT NULL,
	constraint supplier_pkey primary key (s_suppkey),
	constraint fk_supplier foreign key (s_nationkey)
		references public.nation (n_nationkey) match simple
		on update no action
		on delete no action
)
WITH (
	OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.supplier
	OWNER to postgres;



CREATE TABLE IF NOT EXISTS public.partsupp
(
	ps_partkey integer NOT NULL,
	ps_suppkey integer NOT NULL,
	ps_availqty integer NOT NULL,
	ps_supplycost numeric(15,2) not null,
	ps_comment character varying(199) COLLATE pg_catalog."default" NOT NULL,
	constraint partsupp_pkey primary key (ps_partkey, ps_suppkey),
	constraint fk_ps_suppkey_partkey foreign key (ps_partkey)
		references public.part (p_partkey) match simple
		on update no action
		on delete no action,
	constraint fk_ps_suppkey_suppkey foreign key (ps_suppkey)
		references public.supplier (s_suppkey) match simple
		on update no action
		on delete no action
)
WITH (
	OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.partsupp
	OWNER to postgres;



CREATE TABLE IF NOT EXISTS public.customer
(
	c_custkey integer NOT NULL,
	c_name character varying(25) COLLATE pg_catalog."default" NOT NULL,
	c_address character varying(40) COLLATE pg_catalog."default" NOT NULL,
	c_nationkey integer NOT NULL,
	c_phone character(15) COLLATE pg_catalog."default" NOT NULL,
	c_acctbal numeric(15,2) not null,
	c_mktsegment character(10) COLLATE pg_catalog."default" NOT NULL,
	c_comment character varying(117) COLLATE pg_catalog."default" NOT NULL,
	constraint customer_pkey primary key (c_custkey),
	constraint fk_customer foreign key (c_nationkey)
		references public.nation (n_nationkey) match simple
		on update no action
		on delete no action
)
WITH (
	OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.customer
	OWNER to postgres;



CREATE TABLE IF NOT EXISTS public.orders
(
	o_orderkey integer NOT NULL,
	o_custkey integer NOT NULL,
	o_orderstatus character(1) COLLATE pg_catalog."default" NOT NULL,
	o_totalprice numeric(15,2) not null,
	o_orderdate date not null,
	o_orderpriority character(15) COLLATE pg_catalog."default" NOT NULL,
	o_clerk character(15) COLLATE pg_catalog."default" NOT NULL,
	o_shippriority integer NOT NULL,
	o_comment character varying(79) COLLATE pg_catalog."default" NOT NULL,
	constraint orders_pkey primary key (o_orderkey),
	constraint fk_orders foreign key (o_custkey)
		references public.customer (c_custkey) match simple
		on update no action
		on delete no action
)
WITH (
	OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.orders
	OWNER to postgres;



CREATE TABLE IF NOT EXISTS public.lineitem
(
	l_orderkey integer NOT NULL,
	l_partkey integer NOT NULL,
	l_suppkey integer NOT NULL,
	l_linenumber integer NOT NULL,
	l_quantity numeric(15,2) not null,
	l_extendedprice numeric(15,2) not null,
	l_discount numeric(15,2) not null,
	l_tax numeric(15,2) not null,
	l_returnflag character(1) COLLATE pg_catalog."default" NOT NULL,
	l_linestatus character(1) COLLATE pg_catalog."default" NOT NULL,
	l_shipdate date not null,
	l_commitdate date not null,
	l_receiptdate date not null,
	l_shipinstruct character(25) COLLATE pg_catalog."default" NOT NULL,
	l_shipmode character(10) COLLATE pg_catalog."default" NOT NULL,
	l_comment character varying(44) COLLATE pg_catalog."default" NOT NULL,
	constraint lineitem_pkey primary key (l_orderkey, l_partkey, l_suppkey, l_linenumber),
	constraint fk_lineitem_orderkey foreign key (l_orderkey)
		references public.orders (o_orderkey) match simple
		on update no action
		on delete no action,
	constraint fk_lineitem_partkey foreign key (l_partkey)
		references public.part (p_partkey) match simple
		on update no action
		on delete no action,
	constraint fk_lineitem_suppkey foreign key (l_suppkey)
		references public.supplier (s_suppkey) match simple
		on update no action
		on delete no action
)
WITH (
	OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.lineitem
	OWNER to postgres;



