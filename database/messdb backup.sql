--
-- PostgreSQL database dump
--

-- Dumped from database version 17.4
-- Dumped by pg_dump version 17.2

-- Started on 2025-04-26 18:00:01

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 228 (class 1259 OID 24760)
-- Name: Attendance; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Attendance" (
    attendance_id integer NOT NULL,
    user_id integer NOT NULL,
    meal_id integer NOT NULL,
    status character varying(50)
);


ALTER TABLE public."Attendance" OWNER TO postgres;

--
-- TOC entry 227 (class 1259 OID 24759)
-- Name: Attendance_attendance_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."Attendance_attendance_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public."Attendance_attendance_id_seq" OWNER TO postgres;

--
-- TOC entry 4953 (class 0 OID 0)
-- Dependencies: 227
-- Name: Attendance_attendance_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."Attendance_attendance_id_seq" OWNED BY public."Attendance".attendance_id;


--
-- TOC entry 226 (class 1259 OID 24748)
-- Name: Billing; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Billing" (
    bill_id integer NOT NULL,
    user_id integer NOT NULL,
    month character varying(20) NOT NULL,
    total_meals integer,
    total_breakfasts integer,
    amount numeric(10,2),
    generated_on date,
    is_paid boolean
);


ALTER TABLE public."Billing" OWNER TO postgres;

--
-- TOC entry 225 (class 1259 OID 24747)
-- Name: Billing_bill_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."Billing_bill_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public."Billing_bill_id_seq" OWNER TO postgres;

--
-- TOC entry 4954 (class 0 OID 0)
-- Dependencies: 225
-- Name: Billing_bill_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."Billing_bill_id_seq" OWNED BY public."Billing".bill_id;


--
-- TOC entry 222 (class 1259 OID 24729)
-- Name: Inventory; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Inventory" (
    item_id integer NOT NULL,
    name character varying(255),
    unit character varying(50),
    quantity integer,
    updated_on date
);


ALTER TABLE public."Inventory" OWNER TO postgres;

--
-- TOC entry 221 (class 1259 OID 24728)
-- Name: Inventory_item_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."Inventory_item_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public."Inventory_item_id_seq" OWNER TO postgres;

--
-- TOC entry 4955 (class 0 OID 0)
-- Dependencies: 221
-- Name: Inventory_item_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."Inventory_item_id_seq" OWNED BY public."Inventory".item_id;


--
-- TOC entry 224 (class 1259 OID 24736)
-- Name: MealInstance; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."MealInstance" (
    meal_id integer NOT NULL,
    menu_id integer NOT NULL,
    date date NOT NULL
);


ALTER TABLE public."MealInstance" OWNER TO postgres;

--
-- TOC entry 223 (class 1259 OID 24735)
-- Name: MealInstance_meal_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."MealInstance_meal_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public."MealInstance_meal_id_seq" OWNER TO postgres;

--
-- TOC entry 4956 (class 0 OID 0)
-- Dependencies: 223
-- Name: MealInstance_meal_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."MealInstance_meal_id_seq" OWNED BY public."MealInstance".meal_id;


--
-- TOC entry 218 (class 1259 OID 24709)
-- Name: Users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Users" (
    user_id integer NOT NULL,
    email character varying(255) NOT NULL,
    role character varying(50),
    password character varying(255)
);


ALTER TABLE public."Users" OWNER TO postgres;

--
-- TOC entry 217 (class 1259 OID 24708)
-- Name: Users_user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."Users_user_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public."Users_user_id_seq" OWNER TO postgres;

--
-- TOC entry 4957 (class 0 OID 0)
-- Dependencies: 217
-- Name: Users_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."Users_user_id_seq" OWNED BY public."Users".user_id;


--
-- TOC entry 220 (class 1259 OID 24720)
-- Name: WeeklyMenu; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."WeeklyMenu" (
    menu_id integer NOT NULL,
    weekday character varying(10) NOT NULL,
    meal_type character varying(50) NOT NULL,
    items character varying
);


ALTER TABLE public."WeeklyMenu" OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 24719)
-- Name: WeeklyMenu_menu_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."WeeklyMenu_menu_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public."WeeklyMenu_menu_id_seq" OWNER TO postgres;

--
-- TOC entry 4958 (class 0 OID 0)
-- Dependencies: 219
-- Name: WeeklyMenu_menu_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."WeeklyMenu_menu_id_seq" OWNED BY public."WeeklyMenu".menu_id;


--
-- TOC entry 4772 (class 2604 OID 24763)
-- Name: Attendance attendance_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Attendance" ALTER COLUMN attendance_id SET DEFAULT nextval('public."Attendance_attendance_id_seq"'::regclass);


--
-- TOC entry 4771 (class 2604 OID 24751)
-- Name: Billing bill_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Billing" ALTER COLUMN bill_id SET DEFAULT nextval('public."Billing_bill_id_seq"'::regclass);


--
-- TOC entry 4769 (class 2604 OID 24732)
-- Name: Inventory item_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Inventory" ALTER COLUMN item_id SET DEFAULT nextval('public."Inventory_item_id_seq"'::regclass);


--
-- TOC entry 4770 (class 2604 OID 24739)
-- Name: MealInstance meal_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."MealInstance" ALTER COLUMN meal_id SET DEFAULT nextval('public."MealInstance_meal_id_seq"'::regclass);


--
-- TOC entry 4767 (class 2604 OID 24712)
-- Name: Users user_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Users" ALTER COLUMN user_id SET DEFAULT nextval('public."Users_user_id_seq"'::regclass);


--
-- TOC entry 4768 (class 2604 OID 24723)
-- Name: WeeklyMenu menu_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."WeeklyMenu" ALTER COLUMN menu_id SET DEFAULT nextval('public."WeeklyMenu_menu_id_seq"'::regclass);


--
-- TOC entry 4947 (class 0 OID 24760)
-- Dependencies: 228
-- Data for Name: Attendance; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 4945 (class 0 OID 24748)
-- Dependencies: 226
-- Data for Name: Billing; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 4941 (class 0 OID 24729)
-- Dependencies: 222
-- Data for Name: Inventory; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 4943 (class 0 OID 24736)
-- Dependencies: 224
-- Data for Name: MealInstance; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 4937 (class 0 OID 24709)
-- Dependencies: 218
-- Data for Name: Users; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public."Users" VALUES (1, 'john.doe@example.com', 'admin', 'hashedpassword123');
INSERT INTO public."Users" VALUES (2, 'ligma@email.com', 'chicken nugget scientist', 'password');
INSERT INTO public."Users" VALUES (3, 'chigma@pigma.com', 'zaidi cake eater', 'password');


--
-- TOC entry 4939 (class 0 OID 24720)
-- Dependencies: 220
-- Data for Name: WeeklyMenu; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public."WeeklyMenu" VALUES (1, 'Monday', 'Lunch', 'Rice, Dal, Paneer');
INSERT INTO public."WeeklyMenu" VALUES (2, 'Tuesday', 'Lunch', 'Lobia, Roti, Achar');
INSERT INTO public."WeeklyMenu" VALUES (3, 'Wednesday', 'Dinner', 'Shashlik, Fried Rice');


--
-- TOC entry 4959 (class 0 OID 0)
-- Dependencies: 227
-- Name: Attendance_attendance_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."Attendance_attendance_id_seq"', 1, false);


--
-- TOC entry 4960 (class 0 OID 0)
-- Dependencies: 225
-- Name: Billing_bill_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."Billing_bill_id_seq"', 1, false);


--
-- TOC entry 4961 (class 0 OID 0)
-- Dependencies: 221
-- Name: Inventory_item_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."Inventory_item_id_seq"', 1, false);


--
-- TOC entry 4962 (class 0 OID 0)
-- Dependencies: 223
-- Name: MealInstance_meal_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."MealInstance_meal_id_seq"', 1, false);


--
-- TOC entry 4963 (class 0 OID 0)
-- Dependencies: 217
-- Name: Users_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."Users_user_id_seq"', 3, true);


--
-- TOC entry 4964 (class 0 OID 0)
-- Dependencies: 219
-- Name: WeeklyMenu_menu_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."WeeklyMenu_menu_id_seq"', 3, true);


--
-- TOC entry 4786 (class 2606 OID 24765)
-- Name: Attendance Attendance_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Attendance"
    ADD CONSTRAINT "Attendance_pkey" PRIMARY KEY (attendance_id);


--
-- TOC entry 4784 (class 2606 OID 24753)
-- Name: Billing Billing_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Billing"
    ADD CONSTRAINT "Billing_pkey" PRIMARY KEY (bill_id);


--
-- TOC entry 4780 (class 2606 OID 24734)
-- Name: Inventory Inventory_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Inventory"
    ADD CONSTRAINT "Inventory_pkey" PRIMARY KEY (item_id);


--
-- TOC entry 4782 (class 2606 OID 24741)
-- Name: MealInstance MealInstance_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."MealInstance"
    ADD CONSTRAINT "MealInstance_pkey" PRIMARY KEY (meal_id);


--
-- TOC entry 4774 (class 2606 OID 24718)
-- Name: Users Users_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Users"
    ADD CONSTRAINT "Users_email_key" UNIQUE (email);


--
-- TOC entry 4776 (class 2606 OID 24716)
-- Name: Users Users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Users"
    ADD CONSTRAINT "Users_pkey" PRIMARY KEY (user_id);


--
-- TOC entry 4778 (class 2606 OID 24727)
-- Name: WeeklyMenu WeeklyMenu_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."WeeklyMenu"
    ADD CONSTRAINT "WeeklyMenu_pkey" PRIMARY KEY (menu_id);


--
-- TOC entry 4789 (class 2606 OID 24771)
-- Name: Attendance Attendance_meal_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Attendance"
    ADD CONSTRAINT "Attendance_meal_id_fkey" FOREIGN KEY (meal_id) REFERENCES public."MealInstance"(meal_id);


--
-- TOC entry 4790 (class 2606 OID 24766)
-- Name: Attendance Attendance_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Attendance"
    ADD CONSTRAINT "Attendance_user_id_fkey" FOREIGN KEY (user_id) REFERENCES public."Users"(user_id);


--
-- TOC entry 4788 (class 2606 OID 24754)
-- Name: Billing Billing_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Billing"
    ADD CONSTRAINT "Billing_user_id_fkey" FOREIGN KEY (user_id) REFERENCES public."Users"(user_id);


--
-- TOC entry 4787 (class 2606 OID 24742)
-- Name: MealInstance MealInstance_menu_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."MealInstance"
    ADD CONSTRAINT "MealInstance_menu_id_fkey" FOREIGN KEY (menu_id) REFERENCES public."WeeklyMenu"(menu_id);


-- Completed on 2025-04-26 18:00:01

--
-- PostgreSQL database dump complete
--

