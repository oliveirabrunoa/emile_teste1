from ldap3 import Server, Connection, ALL, ALL_ATTRIBUTES


class LDAPAuthenticationBackend:

    def authenticate(self, email, password):
        try:
            server = Server(host='10.1.0.4', get_info=ALL)
            conn = Connection(server, user=email, password=password, auto_bind=True)
            conn.search(search_base='DC=intranet, DC=cefetba, DC=br',
                        search_filter='(sAMAccountName={0})'.format(str(email).split('@')[0]),
                        attributes=ALL_ATTRIBUTES)
            return "[" + conn.entries[0].entry_to_json() + "]", 200
        except Exception as e:
            return str(e), 401
