\set ON_ERROR_STOP on

BEGIN;

ALTER SCHEMA public OWNER TO peng;

ALTER TABLE public.ikan OWNER TO peng;
ALTER TABLE public.riwayat_kematian OWNER TO peng;
ALTER TABLE public.riwayat_penjualan OWNER TO peng;
ALTER TABLE public.ceo_accounts OWNER TO peng;

ALTER SEQUENCE public.ikan_id_seq OWNER TO peng;
ALTER SEQUENCE public.riwayat_kematian_id_seq OWNER TO peng;
ALTER SEQUENCE public.riwayat_penjualan_id_seq OWNER TO peng;
ALTER SEQUENCE public.ceo_accounts_id_seq OWNER TO peng;

ALTER FUNCTION public.update_updated_at() OWNER TO peng;
ALTER FUNCTION public.set_ceo_updated_at() OWNER TO peng;

COMMIT;
