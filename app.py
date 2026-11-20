import streamlit as st
from web3 import Web3
import plotly.express as px
import json
import os
import urllib.parse
import pandas as pd
from datetime import datetime

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="E-Voting Terdesentralisasi",
    page_icon="🗳️",
    layout="wide"
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# --- CSS TEMA NAVY DARK MODE ---
st.markdown("""
    <style>
    .stApp, header[data-testid="stHeader"] { background-color: #0E1629 !important; }
    section[data-testid="stSidebar"] { background-color: #162038 !important; }
    
    /* Warna teks utama putih terang */
    h1, h2, h3, h4, p, label, li, strong, span, small,
    div[data-testid="stMarkdownContainer"],
    div[data-testid="stMetricValue"], div[data-testid="stMetricLabel"],
    div[data-testid="stCaptionContainer"] {
        color: #FFFFFF !important;
    }

    /* Kode & Hash */
    code {
        background-color: #1E293B !important;
        color: #38BDF8 !important;
        border: 1px solid #334155 !important;
        padding: 2px 6px !important;
        border-radius: 4px !important;
    }

    /* Tombol Umum */
    .stButton > button, div[data-testid="stFormSubmitButton"] > button, .stDownloadButton > button {
        background-color: #1E293B !important;
        border: 1px solid #38BDF8 !important;
    }
    .stButton > button p, .stButton > button span,
    div[data-testid="stFormSubmitButton"] > button p, div[data-testid="stFormSubmitButton"] > button span,
    .stDownloadButton > button p, .stDownloadButton > button span {
        color: #FFFFFF !important;
        font-weight: 700 !important;
    }

    /* Kotak Input Teks & TextArea */
    .stTextInput input, .stTextArea textarea {
        color: #1E1E1E !important;
        background-color: #F1F5F9 !important;
        font-weight: 600 !important;
    }

    /* Selectbox / Dropdown */
    div[data-baseweb="select"] > div {
        background-color: #F1F5F9 !important;
    }
    div[data-baseweb="select"] span, div[data-baseweb="select"] div {
        color: #1E1E1E !important;
        font-weight: 600 !important;
    }
    ul[data-baseweb="menu"] li, ul[data-baseweb="menu"] li span {
        color: #1E1E1E !important;
        background-color: #FFFFFF !important;
    }

    /* Kotak File Uploader */
    section[data-testid="stFileUploaderDropzone"] {
        background-color: #1E293B !important;
        border: 1px dashed #38BDF8 !important;
    }
    section[data-testid="stFileUploaderDropzone"] span,
    section[data-testid="stFileUploaderDropzone"] small,
    section[data-testid="stFileUploaderDropzone"] div {
        color: #FFFFFF !important;
    }
    section[data-testid="stFileUploaderDropzone"] button {
        background-color: #0284C7 !important;
        color: #FFFFFF !important;
        border: none !important;
    }

    /* Kotak Alert (Success, Warning, Error, Info) */
    div[data-testid="stAlert"] {
        background-color: #1E293B !important;
        border-left: 5px solid #38BDF8 !important;
    }
    div[data-testid="stAlert"] p, div[data-testid="stAlert"] span, div[data-testid="stAlert"] div {
        color: #FFFFFF !important;
        font-weight: 600 !important;
    }
    </style>
""", unsafe_allow_html=True)

if "confirm_vote_id" not in st.session_state:
    st.session_state.confirm_vote_id = None
if "last_tx_status" not in st.session_state:
    st.session_state.last_tx_status = None

# --- KONEKSI BLOCKCHAIN MENGGUNAKAN WEB3.PY ---
HARDHAT_URL = "http://127.0.0.1:8545"
w3 = Web3(Web3.HTTPProvider(HARDHAT_URL))

@st.cache_resource
def load_contract():
    try:
        with open("deployment.json", "r") as f:
            contract_address = json.load(f).get("address")
        with open("artifacts/contracts/EVotingHIMAFOR.sol/EVotingHIMAFOR.json", "r") as f:
            abi = json.load(f)["abi"]
        return w3.eth.contract(address=Web3.to_checksum_address(contract_address), abi=abi), contract_address
    except Exception as e:
        st.error(f"Gagal memuat Smart Contract: {e}")
        return None, None

contract, contract_address = load_contract()
node_online = w3.is_connected()

def get_candidate_photo(candidate_id, name):
    for ext in ["png", "jpg", "jpeg"]:
        local_path = os.path.join(UPLOAD_DIR, f"kandidat_{candidate_id}.{ext}")
        if os.path.exists(local_path):
            return local_path
    encoded = urllib.parse.quote(name)
    return f"https://ui-avatars.com/api/?name={encoded}&background=0284C7&color=FFFFFF&size=256&bold=true"

def fetch_blockchain_data():
    candidates = []
    votes = []
    voted_wallets = set()

    if contract and node_online:
        try:
            total_candidates = contract.functions.candidateCount().call()

            for i in range(1, total_candidates + 1):
                rec_id, nama, visi, misi, jumlah_suara = (
                    contract.functions.getCandidate(i).call()
                )

                candidates.append({
                    "ID": rec_id,
                    "Nama Kandidat": nama,
                    "Visi & Misi": f"Visi: {visi} | Misi: {misi}",
                    "Foto": get_candidate_photo(rec_id, nama),
                    "Waktu Daftar": "Tercatat di Blockchain",
                    "Pendaftar": "Admin HIMAFOR",
                    "Suara": jumlah_suara
                })

            vote_events = contract.events.VoteCast.get_logs(
                from_block=0,
                to_block="latest"
            )

            for event in vote_events:
                candidate_id = event["args"]["candidateId"]
                voter = event["args"]["voter"]

                candidate_name = next(
                    (
                        c["Nama Kandidat"]
                        for c in candidates
                        if c["ID"] == candidate_id
                    ),
                    "Tidak diketahui"
                )

                block = w3.eth.get_block(event["blockNumber"])
                waktu = datetime.fromtimestamp(
                    block["timestamp"]
                ).strftime("%Y-%m-%d %H:%M:%S")

                votes.append({
                    "Tx ID": event["transactionHash"].hex(),
                    "ID Kandidat": candidate_id,
                    "Nama Kandidat": candidate_name,
                    "Wallet Pemilih": voter,
                    "Waktu Voting": waktu
                })

                voted_wallets.add(voter.lower())

        except Exception as e:
            st.error(f"Gagal membaca data dari Smart Contract: {repr(e)}")

    return candidates, votes, voted_wallets

candidates_data, votes_data, voted_wallets_set = fetch_blockchain_data()

# --- SIDEBAR ---
with st.sidebar:
    st.title("🗳️ E-Voting DApp")
    menu = st.radio(
        "Navigasi Halaman:",
        ["1. Dashboard", "2. Candidate List & Detail", "3. Form Input Kandidat", "4. Voting Page", "5. Results & Verification", "6. Admin Panel"]
    )
    st.markdown("---")
    st.subheader("🔌 Status Jaringan")
    if node_online and contract_address:
        st.success("🟢 Hardhat Node Connected")
        st.caption(f"Contract: `{contract_address[:12]}...`")
    else:
        st.error("🔴 Blockchain Disconnected")

    st.markdown("---")
    st.subheader("👛 Koneksi Wallet")
    user_wallet = st.text_input("Alamat Wallet (Hardhat):", placeholder="0x...").strip()

    wallet_valid = False
    has_voted = False
    if user_wallet:
        if w3.is_address(user_wallet):
            wallet_valid = True
            has_voted = user_wallet.lower() in voted_wallets_set
            st.info("Wallet Valid ✅")
            try:
                bal = w3.from_wei(w3.eth.get_balance(Web3.to_checksum_address(user_wallet)), "ether")
                st.caption(f"Saldo: **{bal:.2f} ETH**")
            except Exception:
                pass
        else:
            st.error("Alamat wallet tidak valid!")

# --- HALAMAN 1: DASHBOARD ---
if menu == "1. Dashboard":
    st.title("📊 Dashboard E-Voting Terdesentralisasi")
    st.markdown("Sistem pemungutan suara digital transparan yang terhubung ke Smart Contract Ethereum menggunakan **Web3.py**.")
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Jumlah Kandidat", f"{len(candidates_data)} Paslon")
    col2.metric("Total Suara Masuk", f"{len(votes_data)} Suara")
    col3.metric("Total Pemilih Unik", f"{len(voted_wallets_set)} Wallet")
    col4.metric("Status Pemilihan", "🟢 Aktif Berlangsung" if candidates_data else "🟡 Menunggu Kandidat")
    st.markdown("---")
    st.write(f"- **Alamat Contract:** `{contract_address}`")
    st.write(f"- **RPC Network:** `{HARDHAT_URL}`")

# --- HALAMAN 2: CANDIDATE LIST & DETAIL ---
elif menu == "2. Candidate List & Detail":
    st.title("👥 Daftar Kandidat & Detail Data")
    st.markdown("---")
    if not candidates_data:
        st.warning("Belum ada kandidat terdaftar.")
    else:
        cols = st.columns(min(len(candidates_data), 3))
        for idx, c in enumerate(candidates_data):
            with cols[idx % 3]:
                with st.container(border=True):
                    st.image(c["Foto"], width=150)
                    st.markdown(f"### Kandidat #{c['ID']}")
                    st.markdown(f"#### **{c['Nama Kandidat']}**")
                    st.write(f"**Visi & Misi:** {c['Visi & Misi']}")
                    st.caption(f"Perolehan: **{c['Suara']} Suara**")
        st.markdown("---")
        st.dataframe(pd.DataFrame(candidates_data)[["ID", "Nama Kandidat", "Visi & Misi", "Suara", "Waktu Daftar"]], use_container_width=True, hide_index=True)

        selected_id = st.selectbox("Pilih ID Kandidat untuk detail:", options=[c["ID"] for c in candidates_data])
        detail = next(c for c in candidates_data if c["ID"] == selected_id)
        with st.container(border=True):
            c_img, c_info = st.columns([1, 3])
            with c_img:
                st.image(detail["Foto"], width=160)
            with c_info:
                st.write(f"**ID Blockchain:** `{detail['ID']}`")
                st.write(f"**Nama Kandidat:** {detail['Nama Kandidat']}")
                st.write(f"**Visi & Misi:** {detail['Visi & Misi']}")
                st.write(f"**Jumlah Suara:** {detail['Suara']} Suara")
                st.write(f"**Pendaftar:** `{detail['Pendaftar']}`")

# --- HALAMAN 3: FORM INPUT KANDIDAT ---
elif menu == "3. Form Input Kandidat":
    st.title("➕ Form Pendaftaran Kandidat Baru")
    st.markdown("---")

    with st.form("form_input_kandidat", clear_on_submit=True):
        nama_baru = st.text_input("Nama Lengkap Kandidat / Paslon *")
        visi_baru = st.text_area("Visi Kandidat *")
        misi_baru = st.text_area("Misi Kandidat *")
        foto_file = st.file_uploader(
            "Upload Foto Kandidat (JPG / PNG)",
            type=["jpg", "jpeg", "png"]
        )

        submit_btn = st.form_submit_button(
            "💾 Simpan Kandidat ke Blockchain"
        )

        if submit_btn:
            if not wallet_valid:
                st.error("Masukkan wallet admin yang valid!")
            elif not nama_baru.strip():
                st.error("Nama kandidat tidak boleh kosong!")
            elif not visi_baru.strip() or not misi_baru.strip():
                st.error("Visi dan misi wajib diisi!")
            else:
                try:
                    admin_address = contract.functions.admin().call()

                    if user_wallet.lower() != admin_address.lower():
                        st.error("Hanya admin yang dapat mendaftarkan kandidat!")
                    else:
                        with st.spinner("Mengirim data ke blockchain..."):
                            tx_hash = contract.functions.registerCandidate(
                                nama_baru.strip(),
                                visi_baru.strip(),
                                misi_baru.strip()
                            ).transact({
                                "from": Web3.to_checksum_address(user_wallet)
                            })

                            receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

                            if foto_file is not None:
                                new_id = contract.functions.candidateCount().call()
                                ext = foto_file.name.split(".")[-1].lower()
                                for old_ext in ["png", "jpg", "jpeg"]:
                                    old_file = os.path.join(UPLOAD_DIR, f"kandidat_{new_id}.{old_ext}")
                                    if os.path.exists(old_file):
                                        os.remove(old_file)
                                save_path = os.path.join(UPLOAD_DIR, f"kandidat_{new_id}.{ext}")
                                with open(save_path, "wb") as f:
                                    f.write(foto_file.getbuffer())

                        st.success(
                            f"Kandidat {nama_baru} berhasil didaftarkan!"
                        )
                        st.code(tx_hash.hex())
                        st.rerun()

                except Exception as e:
                    st.error(f"Transaksi gagal: {e}")

# --- HALAMAN 4: VOTING PAGE ---
elif menu == "4. Voting Page":
    st.title("🗳️ Bilik Pemungutan Suara")
    st.markdown("---")

    if st.session_state.last_tx_status:
        st.success("✅ Pemilihan Berhasil! Suara Anda telah tercatat secara permanen di Blockchain.")
        st.code(f"Transaction Hash: {st.session_state.last_tx_status}")
        st.session_state.last_tx_status = None

    if not wallet_valid:
        st.warning("Wallet belum terhubung.")
    else:
        try:
            registered, verified, already_voted = (
                contract.functions.getVoterStatus(
                    Web3.to_checksum_address(user_wallet)
                ).call()
            )

            if not registered:
                st.warning("Wallet belum terdaftar sebagai pemilih.")
            elif not verified:
                st.warning("Wallet belum diverifikasi oleh admin.")
            elif already_voted:
                st.error("Wallet ini sudah menggunakan hak pilih.")
            else:
                election_open = contract.functions.electionOpen().call()

                if not election_open:
                    st.warning("Pemilihan belum dibuka atau sudah ditutup.")
                else:
                    st.success("Wallet terverifikasi dan dapat melakukan voting.")

                    for c in candidates_data:
                        with st.container(border=True):
                            col_foto, col_detail = st.columns([1, 4])
                            with col_foto:
                                st.image(c["Foto"], width=130)
                            with col_detail:
                                st.subheader(
                                    f"Kandidat #{c['ID']} - {c['Nama Kandidat']}"
                                )
                                st.write(c["Visi & Misi"])
                                st.write(f"Jumlah suara: **{c['Suara']}**")

                                if st.button(
                                    f"Pilih Kandidat #{c['ID']}",
                                    key=f"vote_{c['ID']}"
                                ):
                                    st.session_state.confirm_vote_id = c["ID"]

                    if st.session_state.confirm_vote_id is not None:
                        target = next(
                            (
                                item for item in candidates_data
                                if item["ID"] == st.session_state.confirm_vote_id
                            ),
                            None
                        )

                        if target:
                            st.warning(
                                f"Yakin memilih {target['Nama Kandidat']}?"
                            )

                            col1, col2 = st.columns(2)

                            with col1:
                                if st.button("Ya, Kirim Suara"):
                                    try:
                                        tx_hash = contract.functions.vote(
                                            target["ID"]
                                        ).transact({
                                            "from": Web3.to_checksum_address(
                                                user_wallet
                                            )
                                        })

                                        receipt = w3.eth.wait_for_transaction_receipt(
                                            tx_hash
                                        )

                                        st.session_state.confirm_vote_id = None
                                        st.session_state.last_tx_status = tx_hash.hex()
                                        st.rerun()

                                    except Exception as e:
                                        st.error(f"Voting gagal: {e}")

                            with col2:
                                if st.button("Batal"):
                                    st.session_state.confirm_vote_id = None
                                    st.rerun()

        except Exception as e:
            st.error(f"Gagal memeriksa status pemilih: {e}")

# --- HALAMAN 5: RESULTS & VERIFICATION ---
elif menu == "5. Results & Verification":
    st.title("📈 Hasil Voting & Verifikasi")
    st.markdown("---")

    try:
        election_open = contract.functions.electionOpen().call()

        if election_open:
            st.warning("Pemilihan masih berlangsung. Hasil akhir belum tersedia.")
        else:
            st.success("Pemilihan telah ditutup. Hasil akhir tersedia.")

        if not election_open:
            result_ids, result_names, result_votes = contract.functions.getResults().call()

            if result_ids:
                hasil = []

                for candidate_id, jumlah_suara in zip(
                    result_ids, result_votes
                ):
                    candidate = contract.functions.getCandidate(
                        candidate_id
                    ).call()

                    hasil.append({
                        "ID Kandidat": candidate_id,
                        "Nama Kandidat": candidate[1],
                        "Jumlah Suara": jumlah_suara
                    })

                df_hasil = pd.DataFrame(hasil)

                st.subheader("Hasil Akhir Pemilihan")
                st.dataframe(
                    df_hasil,
                    use_container_width=True,
                    hide_index=True
                )

                fig = px.bar(
                    df_hasil,
                    x="Nama Kandidat",
                    y="Jumlah Suara",
                    color="Nama Kandidat",
                    text_auto=True
                )

                fig.update_layout(
                    paper_bgcolor="#0E1629",
                    plot_bgcolor="#162038",
                    font_color="#FFFFFF"
                )

                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Belum ada hasil pemilihan.")

        st.markdown("---")
        st.subheader("Status Pemilih Saat Ini")

        if wallet_valid:
            registered, verified, already_voted = (
                contract.functions.getVoterStatus(
                    Web3.to_checksum_address(user_wallet)
                ).call()
            )

            st.write(f"**Wallet:** `{user_wallet}`")
            st.write(
                f"**Terdaftar:** {'Ya' if registered else 'Tidak'}"
            )
            st.write(
                f"**Terverifikasi:** {'Ya' if verified else 'Tidak'}"
            )
            st.write(
                f"**Sudah Voting:** {'Ya' if already_voted else 'Belum'}"
            )
        else:
            st.info("Masukkan alamat wallet di Sidebar untuk melihat status.")

        st.markdown("---")
        st.subheader("Riwayat Transaksi Voting")

        if votes_data:
            st.dataframe(
                pd.DataFrame(votes_data),
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("Belum ada transaksi voting.")

    except Exception as e:
        st.error(f"Gagal mengambil hasil voting: {e}")

# --- HALAMAN 6: ADMIN PANEL ---
elif menu == "6. Admin Panel":
    st.title("⚙️ Admin Panel HIMAFOR")
    st.markdown("---")

    if not wallet_valid:
        st.warning("Hubungkan wallet admin terlebih dahulu.")
    else:
        try:
            admin_address = contract.functions.admin().call()

            if user_wallet.lower() != admin_address.lower():
                st.error("Akses ditolak! Halaman ini hanya untuk admin.")
            else:
                st.success("Admin berhasil terhubung.")

                election_open = contract.functions.electionOpen().call()

                st.write(f"**Alamat Admin:** `{admin_address}`")
                st.write(
                    f"**Status Pemilihan:** {'🟢 Terbuka' if election_open else '🔴 Tertutup'}"
                )

                st.markdown("---")
                st.subheader("1. Registrasi Pemilih")

                voter_address = st.text_input(
                    "Alamat Wallet Pemilih",
                    key="register_voter"
                ).strip()

                if st.button("Daftarkan Pemilih"):
                    if not w3.is_address(voter_address):
                        st.error("Alamat wallet tidak valid!")
                    else:
                        reg, ver, vot = contract.functions.getVoterStatus(
                            Web3.to_checksum_address(voter_address)
                        ).call()
                        if reg:
                            st.warning("⚠️ Alamat wallet ini sudah terdaftar sebelumnya!")
                        else:
                            tx = contract.functions.registerVoter(
                                Web3.to_checksum_address(voter_address)
                            ).transact({"from": admin_address})

                            receipt = w3.eth.wait_for_transaction_receipt(tx)
                            st.success("✅ Pemilih berhasil didaftarkan!")
                            st.code(tx.hex())

                st.markdown("---")
                st.subheader("2. Verifikasi Pemilih")

                verify_address = st.text_input(
                    "Alamat Wallet untuk Diverifikasi",
                    key="verify_voter"
                ).strip()

                if st.button("Verifikasi Pemilih"):
                    if not w3.is_address(verify_address):
                        st.error("Alamat wallet tidak valid!")
                    else:
                        reg, ver, vot = contract.functions.getVoterStatus(
                            Web3.to_checksum_address(verify_address)
                        ).call()
                        if not reg:
                            st.warning("⚠️ E-Wallet belum terdaftar! Silakan daftarkan terlebih dahulu di bagian Registrasi Pemilih.")
                        elif ver:
                            st.info("ℹ️ Wallet ini sudah terverifikasi sebelumnya.")
                        else:
                            tx = contract.functions.verifyVoter(
                                Web3.to_checksum_address(verify_address)
                            ).transact({"from": admin_address})

                            receipt = w3.eth.wait_for_transaction_receipt(tx)
                            st.success("✅ Pemilih berhasil diverifikasi!")
                            st.code(tx.hex())

                st.markdown("---")
                st.subheader("3. Pengaturan Pemilihan")

                if not election_open:
                    if st.button("🟢 Buka Pemilihan"):
                        tx = contract.functions.openElection().transact(
                            {"from": admin_address}
                        )
                        w3.eth.wait_for_transaction_receipt(tx)
                        st.success("Pemilihan berhasil dibuka!")
                        st.rerun()
                else:
                    if st.button("🔴 Tutup Pemilihan"):
                        tx = contract.functions.closeElection().transact(
                            {"from": admin_address}
                        )
                        w3.eth.wait_for_transaction_receipt(tx)
                        st.success("Pemilihan berhasil ditutup!")
                        st.rerun()

        except Exception as e:
            st.error(f"Terjadi kesalahan: {e}")