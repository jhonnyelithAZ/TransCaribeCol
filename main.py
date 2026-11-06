import os

# Base de datos en memoria (Lista de diccionarios / Matriz)
lista_empleados = []
NOMBRE_ARCHIVO = "nomina.txt"

# Constantes para Administrativos
TARIFA_HORA_ADMIN = 20000
TARIFA_HORA_EXTRA_ADMIN = 25000
PCT_SALUD_ADMIN = 0.04
PCT_PENSION_ADMIN = 0.04
PCT_ARL_ADMIN = 0.00522  # Riesgo I

# Constantes para Operativos (Prestación de Servicios)
TARIFA_HORA_OPERATIVO = 40000
PCT_IBC = 0.40
PCT_SALUD_OPERATIVO = 0.125
PCT_PENSION_OPERATIVO = 0.16

CARGOS_OPERATIVOS = {
    "1": {"nombre": "Conductor", "horas": 160, "riesgo": "II", "arl_pct": 0.01044},
    "2": {"nombre": "Oficios Generales", "horas": 100, "riesgo": "I", "arl_pct": 0.00522},
    "3": {"nombre": "Vigilancia", "horas": 336, "riesgo": "IV", "arl_pct": 0.04350}
}


def formato_moneda(valor):
    """Formatea valores numéricos con separadores de miles y sin decimales."""
    return f"${round(valor):,}".replace(",", ".")


def registrar_administrativo():
    print("\n" + "=" * 45)
    print("  REGISTRO DE EMPLEADO ADMINISTRATIVO")
    print("=" * 45)
    nombre = input("Nombre completo: ").strip()
    cargo = input("Cargo (ej. Auxiliar Administrativo): ").strip()
    
    while True:
        try:
            horas_trabajadas = float(input("Horas ordinarias trabajadas al mes: "))
            horas_extras = float(input("Horas extras trabajadas: "))
            if horas_trabajadas < 0 or horas_extras < 0:
                print("Las horas no pueden ser negativas.")
                continue
            break
        except ValueError:
            print("Entrada inválida. Ingrese valores numéricos.")

    salario_bruto = horas_trabajadas * TARIFA_HORA_ADMIN
    total_extras = horas_extras * TARIFA_HORA_EXTRA_ADMIN
    base_prestaciones = salario_bruto + total_extras

    salud = base_prestaciones * PCT_SALUD_ADMIN
    pension = base_prestaciones * PCT_PENSION_ADMIN
    arl = base_prestaciones * PCT_ARL_ADMIN
    total_descuentos = salud + pension
    total_a_pagar = base_prestaciones - total_descuentos - arl

    empleado = {
        "nombre": nombre,
        "tipo": "ADMINISTRATIVO",
        "cargo": cargo,
        "ht": horas_trabajadas,
        "salario": salario_bruto,
        "he": horas_extras,
        "tphe": total_extras,
        "salud": salud,
        "pension": pension,
        "arl": arl,
        "total_descuentos": total_descuentos,
        "total_a_pagar": total_a_pagar
    }

    lista_empleados.append(empleado)
    print("\n✓ Empleado administrativo registrado con éxito.")
    imprimir_volante_administrativo(empleado)


def registrar_operativo():
    print("\n" + "=" * 45)
    print("  REGISTRO DE EMPLEADO OPERATIVO")
    print("=" * 45)
    nombre = input("Nombre completo: ").strip()
    
    print("\nSeleccione el cargo operativo:")
    print("1. Conductor (160 horas - Riesgo II: 1.044%)")
    print("2. Oficios Generales (100 horas - Riesgo I: 0.522%)")
    print("3. Vigilancia (336 horas - Riesgo IV: 4.350%)")
    
    while True:
        opc_cargo = input("Opción (1-3): ").strip()
        if opc_cargo in CARGOS_OPERATIVOS:
            cargo_info = CARGOS_OPERATIVOS[opc_cargo]
            break
        print("Opción inválida. Ingrese 1, 2 o 3.")

    cargo = cargo_info["nombre"]
    horas_trabajadas = cargo_info["horas"]
    salario_bruto = horas_trabajadas * TARIFA_HORA_OPERATIVO
    horas_extras = 0
    total_extras = 0

    # Base de Cotización (IBC al 40%)
    ibc = salario_bruto * PCT_IBC
    salud = ibc * PCT_SALUD_OPERATIVO
    pension = ibc * PCT_PENSION_OPERATIVO
    arl = ibc * cargo_info["arl_pct"]
    total_aportes = salud + pension + arl
    total_a_pagar = salario_bruto - total_aportes

    empleado = {
        "nombre": nombre,
        "tipo": "OPERATIVO",
        "cargo": cargo,
        "ht": horas_trabajadas,
        "salario": salario_bruto,
        "he": horas_extras,
        "tphe": total_extras,
        "salud": salud,
        "pension": pension,
        "arl": arl,
        "total_descuentos": total_aportes,
        "total_a_pagar": total_a_pagar
    }

    lista_empleados.append(empleado)
    print("\n✓ Empleado operativo registrado con éxito.")
    imprimir_volante_operativo(empleado)


def imprimir_volante_administrativo(emp):
    print("\n" + "*" * 49)
    print("***************** VOLANTE DE PAGO *****************")
    print("*" * 49)
    print(f"Nombre: {emp['nombre']}")
    print(f"Cargo: {emp['cargo']}")
    print(f"Horas Trabajadas(mes): {int(emp['ht'])}")
    print(f"Salario Bruto: {formato_moneda(emp['salario'])}")
    print(f"Horas Extras: {int(emp['he'])}")
    print(f"Total pago Horas Extras: {formato_moneda(emp['tphe'])}")
    print("\n" + "*" * 49)
    print("***************** DESCUENTOS DE LEY ***************")
    print("*" * 49)
    print(f"Salud(4%): {formato_moneda(emp['salud'])}")
    print(f"Pensión(4%): {formato_moneda(emp['pension'])}")
    print(f"ARL(0,522%): {formato_moneda(emp['arl'])}")
    print(f"Total Descuentos: {formato_moneda(emp['total_descuentos'])}")
    print(f"\nTotal a pagar: {formato_moneda(emp['total_a_pagar'])}")
    print("\n" + "*" * 49)
    print("************* FIN DEL VOLANTE DE PAGO *************")
    print("*" * 49 + "\n")


def imprimir_volante_operativo(emp):
    print("\n" + "*" * 49)
    print("***************** VOLANTE DE PAGO *****************")
    print("   (Contrato de Prestación de Servicios - Autónomo)")
    print("*" * 49)
    print(f"Nombre: {emp['nombre']}")
    print(f"Cargo: {emp['cargo']}")
    print(f"Horas Trabajadas(mes): {int(emp['ht'])}")
    print(f"Honorarios Brutos: {formato_moneda(emp['salario'])}")
    print("\n" + "*" * 49)
    print("********** APORTES SEGURIDAD SOCIAL (IBC 40%) ******")
    print("*" * 49)
    print(f"Salud(12.5%): {formato_moneda(emp['salud'])}")
    print(f"Pensión(16%): {formato_moneda(emp['pension'])}")
    print(f"ARL: {formato_moneda(emp['arl'])}")
    print(f"Total Aportes: {formato_moneda(emp['total_descuentos'])}")
    print(f"\nTotal a pagar: {formato_moneda(emp['total_a_pagar'])}")
    print("\n" + "*" * 49)
    print("************* FIN DEL VOLANTE DE PAGO *************")
    print("*" * 49 + "\n")


def mostrar_tabla_nomina():
    if not lista_empleados:
        print("\n[!] No hay empleados registrados en la nómina actual.")
        return

    print("\n" + "=" * 125)
    print(" " * 45 + "TABLA GENERAL DE NÓMINA")
    print("=" * 125)
    header = f"{'Nombre':<25} | {'Tipo':<13} | {'Cargo':<22} | {'HT':<3} | {'Salario':<9} | {'HE':<2} | {'TPHE':<7} | {'Salud':<7} | {'Pension':<7} | {'ARL':<6} | {'Total a pagar':<12}"
    print(header)
    print("-" * 125)

    for emp in lista_empleados:
        row = (
            f"{emp['nombre'][:24]:<25} | "
            f"{emp['tipo']:<13} | "
            f"{emp['cargo'][:21]:<22} | "
            f"{int(emp['ht']):<3} | "
            f"{round(emp['salario']):<9} | "
            f"{int(emp['he']):<2} | "
            f"{round(emp['tphe']):<7} | "
            f"{round(emp['salud']):<7} | "
            f"{round(emp['pension']):<7} | "
            f"{round(emp['arl']):<6} | "
            f"{round(emp['total_a_pagar']):<12}"
        )
        print(row)
    print("=" * 125 + "\n")


def guardar_archivo_txt():
    if not lista_empleados:
        print("\n[!] No hay datos para guardar. Registre empleados primero.")
        return

    with open(NOMBRE_ARCHIVO, "w", encoding="utf-8") as f:
        # Cabecera tabular
        f.write("Nombre\tTipo\tCargo\tHT\tSalario\tHE\tTPHE\tSalud\tPension\tARL\tTotal a pagar\n")
        for emp in lista_empleados:
            linea = f"{emp['nombre']}\t{emp['tipo']}\t{emp['cargo']}\t{int(emp['ht'])}\t{round(emp['salario'])}\t{int(emp['he'])}\t{round(emp['tphe'])}\t{round(emp['salud'])}\t{round(emp['pension'])}\t{round(emp['arl'])}\t{round(emp['total_a_pagar'])}\n"
            f.write(linea)

    print(f"\n✓ Archivo plano '{NOMBRE_ARCHIVO}' guardado exitosamente en memoria secundaria.")


def cargar_y_ver_archivo_txt():
    if not os.path.exists(NOMBRE_ARCHIVO):
        print(f"\n[!] El archivo '{NOMBRE_ARCHIVO}' aún no existe en el disco.")
        return

    print("\n" + "=" * 55)
    print(f" CONTENIDO DEL ARCHIVO PLANO ({NOMBRE_ARCHIVO})")
    print("=" * 55)
    with open(NOMBRE_ARCHIVO, "r", encoding="utf-8") as f:
        contenido = f.read()
        print(contenido)
    print("=" * 55)


def menu_principal():
    while True:
        print("\n" + "=" * 50)
        print("  TRANSCARIBECOL S.C.A. - SISTEMA DE NÓMINA")
        print("=" * 50)
        print("1. Registrar empleado Administrativo")
        print("2. Registrar empleado Operativo")
        print("3. Mostrar tabla de nómina en consola")
        print("4. Guardar nómina en archivo plano (TXT)")
        print("5. Leer archivo plano guardado (TXT)")
        print("6. Salir")
        print("=" * 50)

        opcion = input("Seleccione una opción (1-6): ").strip()

        if opcion == "1":
            registrar_administrativo()
        elif opcion == "2":
            registrar_operativo()
        elif opcion == "3":
            mostrar_tabla_nomina()
        elif opcion == "4":
            guardar_archivo_txt()
        elif opcion == "5":
            cargar_y_ver_archivo_txt()
        elif opcion == "6":
            print("\nGracias por utilizar el sistema de TransCaribeCol. ¡Hasta pronto!")
            break
        else:
            print("\n[!] Opción no válida. Intente nuevamente.")


if __name__ == "__main__":
    menu_principal()