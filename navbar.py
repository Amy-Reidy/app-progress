import dash_bootstrap_components as dbc

def Navbar():
    navbar = dbc.NavbarSimple(
           children=[
              dbc.NavItem(dbc.NavLink("World Bank Index", href="/WBI")),
              dbc.NavItem(dbc.NavLink("RDM Suitability Index", href="/RDM-index")),
              dbc.NavItem(dbc.NavLink("Country Profiles", href="/country-profiles")),
              dbc.NavItem(dbc.NavLink("Time-Series", href="/time-series")),
              dbc.NavItem(dbc.NavLink("Download Data", href="/download-data")),
              dbc.DropdownMenu(
                 nav=True,
                 in_navbar=True,
                 label="Menu",
                 children=[
                    dbc.DropdownMenuItem("Entry 1"),
                    dbc.DropdownMenuItem("Entry 2"),
                    dbc.DropdownMenuItem(divider=True),
                    dbc.DropdownMenuItem("Entry 3"),
                          ],
                      ),
                    ],
          brand="Home",
          brand_href="/home",
          sticky="top")
    return navbar
