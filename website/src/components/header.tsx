import styles from "./header.module.css";
import Link from "next/link";

export default function Header() {
  return (
    <div className={styles.wrapper}>
      <p>Commons GPT PoC</p>
      <div className={styles.links}>
        <Link className={styles.navlink} href="/">
          Home
        </Link>
        <Link className={styles.navlink} href="/about">
          About
        </Link>
      </div>
    </div>
  );
}
